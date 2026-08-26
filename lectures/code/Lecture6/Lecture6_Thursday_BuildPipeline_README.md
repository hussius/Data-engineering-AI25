# Thursday 27/8 — Build your team's pipeline

## Before you start

You should already have, from Wednesday's self-study:

- A free Neon or Supabase project, with a connection string in your own `.env`.
- `db/schema.sql` (from the starter repo) applied against it — `raw__weather`
and `raw__elpris` exist.
- A working `ATTACH ... TYPE postgres` from DuckDB against your own database.

If any of that isn't done, do it first. Follow
`Wed_26_8_Neon_DuckDB_selfstudy.md` again. Everything below assumes it's in
place.

## Goal

Prove the whole loop works end to end, for your team's own assigned station
and price area: call the two source APIs, get raw JSON into your two bronze
tables, in your own cloud Postgres, from a container. Then query what you
landed with DuckDB.

By the end of this session, raw data for your station and area should be sitting 
in your own Postgres.

## This builds on Week 2

Today is the Week 2 pipeline exercise but pointed at new sources and a new
database. Start from that code, not from a blank file:

<https://github.com/hussius/Data-engineering-AI25/tree/main/lectures/code/Lecture4/exercises/pipeline>

Four things will change:

1. **The database has moved to the cloud.** One `DATABASE_URL` instead of five
   `POSTGRES_*` settings.
2. **Two sources instead of one** (neither needs an API key).
3. **No `docker-compose.yml`.** There's no local `db` to orchestrate, so it's
   one container: `docker run --env-file .env`.
4. **The timestamps work differently.** See Task 2.

Everything else — the FastAPI shape, the `Dockerfile`, the postgres connection code -
is code you already have.

## Core tasks (do all four)


### 1. Extend the Week 2 ingestion service

Don't start from a blank file. Copy `ingestion/` from the Week 2 pipeline
exercise linked above — just that subfolder (`Dockerfile`, `ingestion.py`,
`requirements.txt`) — into today's work, and modify it. That's a working
FastAPI service. Today's job is pointing it at two new sources and a
new database, not building the shape from scratch.

Drop `docker-compose.yml` and the `db` and `adminer` services it starts —
you're writing straight to your own Neon/Supabase now — and replace the old
`.env`'s `POSTGRES_*` / `API_URL` / `API_KEY` with the single `DATABASE_URL`
from the starter repo's `.env.example`. That's the same connection string you
already used for Wednesday's DuckDB self-study.

**Where this code lives.** Everything you write today goes in your team repo.
The Week 2 repo is somewhere to copy `ingestion/` *out of*, not somewhere to
work *in*:

```
team1/                    <- your team repo, from the starter template
|-- pyproject.toml
|-- db/schema.sql
|-- model/train.py
|-- data/
`-- ingestion/            <- new today
    |-- ingestion.py
    |-- Dockerfile
    `-- requirements.txt
```

Then point the endpoints at two new places:

- **SMHI observations** (`opendata-download-metobs.smhi.se`), same API you
  used in Week 1, now for your team's assigned station:

  ```
  https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/{param}/station/{station}/period/latest-day/data.json
  ```

  `period/latest-day` is the choice today because it returns a small, recent
  window of JSON. The other ones are unnecessarily large for
  this task but you will have the chance to use them later.

  This API is designed to only return data for one parameter (for example
  temperature), not a whole JSON bundle as with Weather API. So you need
  as many calls per station as there are parameters you want. Today we will fetch
  parameters 1 and 4, air temperature and wind speed, because those are used in
  the pre-provided training code. 


  | `param` | measures | `parameter` column value |
  |---|---|---|
  | `1` | air temperature, instantaneous, hourly | `"temperature"` |
  | `4` | wind speed, 10-min mean | `"wind"` |


- **elprisetjustnu.se**: `https://www.elprisetjustnu.se/api/v1/prices/YYYY/MM-DD_AREA.json`
for your team's assigned price area. No key, same as the curl you ran in
Monday's self-study before the brief was released.

Both are free and key-free — nothing to register today.

**You can iterate outside Docker first.** `ingestion.py`'s `load_dotenv()` already
works fine when you run it directly:

```bash
cd ingestion          # uv walks up to find pyproject.toml, so this is fine
uv run uvicorn ingestion:app --reload --port 8000
# then, in another terminal or browser:
curl "http://localhost:8000/ingestion/electricity?area=SE3&date=2026-08-25"
```

Only containerize (put it into a Docker) once that works — see Task 3.

### 2. Land raw data in your own cloud Postgres

Insert into `raw__weather` and `raw__elpris` exactly as they came back from
the API — JSON payload untouched, in the `data` column. Append-only, same
rule as Week 2: re-ingesting the same station/hour or area/date is allowed
and expected, not an error.

**Connecting.** Here you need only string from your `.env` instead of the
five settings pointing at a local `db` container in last week's code.

```python
import os
import psycopg2
from psycopg2.extras import Json

conn = psycopg2.connect(os.environ["DATABASE_URL"])
```

If `DATABASE_URL` is unset, `psycopg2.connect()` does not fail loudly — it
quietly looks for a local Postgres on a Unix socket instead. An error
mentioning `/var/run/postgresql/.s.PGSQL.5432` always means "the variable
wasn't set", never "the database is down".

#### The simple case — elpris, one row

One request, one row. The whole response array goes into `data` untouched;
the silver layer decides later how to unpack it.

```python
conn = psycopg2.connect(os.environ["DATABASE_URL"])
try:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO raw__elpris (price_area, price_date, data) VALUES (%s, %s, %s)",
            (area, day, Json(payload)),
        )
    conn.commit()
except Exception:
    conn.rollback()
    raise
finally:
    conn.close()
```

Two things there apply to every insert you write today:

- **`%s` for every value, always** — never an f-string, whatever the type.
  psycopg2 does the quoting. Watch the trailing comma in a one-value tuple
  `(area,)`; without it you get a confusing *"not all arguments converted"*.
- **`Json(payload)`** wraps a Python dict or list so it lands in a `jsonb`
  column. Pass the bare dict and you get `can't adapt type 'dict'`.
  (`json.dumps(payload)` does the same job — pick one and be consistent.)

#### The full loop — weather, two calls, many rows

This one is a bit tricky, so here it is end to end. Note that
fetching and inserting are separate functions.

```python
import os
from datetime import datetime, timezone

import psycopg2
import requests
from psycopg2.extras import Json

SMHI_URL = (
    "https://opendata-download-metobs.smhi.se/api/version/1.0"
    "/parameter/{param}/station/{station}/period/latest-day/data.json"
)

# One call per parameter. This is the shape of the API, not a design choice.
PARAMETERS = {1: "temperature", 4: "wind"}


def fetch_weather_rows(station):
    """Both parameters for one station, as rows ready for raw__weather."""
    rows = []
    for param_id, parameter_name in PARAMETERS.items():
        response = requests.get(
            SMHI_URL.format(param=param_id, station=station), timeout=15
        )
        response.raise_for_status()

        for entry in response.json().get("value") or []:
            # SMHI gives epoch MILLISECONDS in UTC, and says so nowhere.
            observed_at = datetime.fromtimestamp(entry["date"] / 1000, tz=timezone.utc)
            rows.append((station, parameter_name, observed_at, Json(entry)))
    return rows


def insert_weather_rows(rows):
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    try:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO raw__weather (station, parameter, observed_at, data) "
                "VALUES (%s, %s, %s, %s)",
                rows,
            )
        conn.commit()
        return len(rows)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
```

Note:

- **Two API calls, not one.** Week 2's weather API handed back all 24 hours in a
  single bundle. SMHI's returns one parameter per request, so a station means
  looping over `PARAMETERS` — two requests, two `parameter` values, same
  table. Write one call and move on, and you'll have temperature but no wind,
  and won't find out until the feature join comes up empty next week.
- **Convert the timestamp before inserting.** SMHI's `date` field is epoch
  *milliseconds* in UTC, so divide by 1000 and pass `tz=timezone.utc`. The
  `observed_at` column is `TIMESTAMPTZ`, which stores an absolute instant —
  insert a naive datetime instead and Postgres assumes the server's timezone,
  your weather lands an hour or two away from the prices it belongs to,
  nothing errors, and the model just gets quietly worse.


#### Check it landed

```sql
SELECT parameter, count(*) FROM raw__weather GROUP BY parameter;
```

Two groups means both calls worked. 

### 3. Containerize it

Same `Dockerfile` you copied from Week 2: dependencies in a cached layer,
code last, nothing to change there. What's different from Week 2 is how you
run it: no `docker compose up` this time, since there's no local `db`
service to orchestrate alongside it. It's one container now, talking
straight out to your cloud Postgres:

```bash
cd ingestion          # same folder as above; the Dockerfile is here
docker build -t ingestion .
docker run --env-file .env -p 8000:8000 ingestion
```

`--env-file .env` is the part that's easy to forget — without it,
`DATABASE_URL` is unset *inside* the container even though it's sitting
right there in your `.env`, and `psycopg2.connect()` silently falls back to
looking for a local Postgres on a Unix socket instead of failing loudly
about a missing variable. If you see an error mentioning
`/var/run/postgresql/.s.PGSQL.5432`, this is why — `--env-file` was left
off.

(If your team prefers `docker compose up` for consistency with Week 2,
that's fine too — just trim `docker-compose.yml` down to the single
`ingestion` service, keeping its `env_file: .env` line, and drop `db` and
`adminer` entirely.)

Confirm `docker build` and `docker run` both work from whoever's laptop
does it — cloud Postgres doesn't care whether the caller is containerized,
only that the connection string and network egress are fine, so if it
worked with plain `uvicorn` above, it'll work here too.

### 4. Query what you landed, with DuckDB

From your Codespace (or local machine), attach your own Postgres and look at
what you just inserted:

```sql
ATTACH 'postgresql://user:pass@host/dbname?sslmode=require' AS pg (TYPE postgres);

SELECT count(*) FROM pg.raw__weather;
SELECT count(*) FROM pg.raw__elpris;
SELECT * FROM pg.raw__weather ORDER BY ingestion_timestamp DESC LIMIT 5;
```

Confirm both tables have rows from your team's own station and area — not
someone else's.


## Afternoon: finish the Sprint 1 backlog and project plan

After lunch (13:00) continue working on the above if not finished.
The last 25 minutes of the day go back to your GitHub
Projects board from Tuesday's planning workshop. **This is due Friday 28/8**
— see `Fri_28_8_selfstudy.md` if you need to finish it outside class time.

Minimum bar for Friday: a written Definition of Done your team actually
agreed on, and a Sprint 1 backlog with real next-tasks (not placeholders) —
including "validate raw data before insert" and "schedule the pipeline to
run daily," since neither is done yet after today.

## Deliverable

Push your containerized ingestion service to your team's repo, on a branch,
PR against `main` with at least one reviewer; same git workflow as Week 2,
now on real project code instead of course material. By end of day your
team's Postgres should have real rows in both bronze tables, reachable from a
teammate's machine, and your Sprint 1 backlog reflects today's actual state
(what's done, what's still open).
