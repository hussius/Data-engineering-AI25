# Wednesday Self-Study: Stand Up Your Own Cloud Postgres

Between Tuesday's project brief release and Thursday, when your team builds
the real pipeline against it.

**Time-box:** 45–60 minutes. Ungraded, no submission — but Thursday assumes
this is already done, individually, by everyone on the team.

## Why this, and why alone first

Thursday's build session is a team session, at tables, with a lot to get
through in 110 minutes. If four or five of you are simultaneously discovering
what a connection string looks like, that's 110 minutes mostly spent on setup
instead of pipeline code. Do the setup once, solo, today — Thursday starts
from "it already works" instead of "let's figure out why it doesn't."

Everyone on the team does this individually, even though you'll likely only
use one team member's database going forward. It's 20 minutes, and knowing
how to do it yourself matters more than not repeating a teammate's step.

## Core (do all three)

### 1. Create a free Postgres project

Pick one — Neon or Supabase, both free, no card:

- **Neon**: [neon.tech](https://neon.tech) → sign up → New Project. You get a
  connection string immediately on the project dashboard.
- **Supabase**: [supabase.com](https://supabase.com) → sign up → New Project.
  Connection string is under **Project Settings → Database → Connection
  string → URI**.

Copy the connection string somewhere safe. It looks like:

```
postgresql://user:password@host/dbname?sslmode=require&channel_binding=require
```

Treat it like a password — because it is one. Don't paste it into a Teams
channel, a commit, or anywhere public.

### 2. Apply the starter schema

Grab `db/schema.sql` from the starter repo (handed out Tuesday afternoon). It
creates two bronze tables — `raw__weather` and `raw__elpris` — the landing
zone for the two data sources your feature pipeline will call tomorrow.

Run it against your new database. Any of these work:

- `psql "**Write your connection string here**" -f db/schema.sql` — runs the file directly,
  no copy-paste. Simplest option if `psql` is available in your Codespace.
- Neon's or Supabase's built-in SQL editor in the browser. There's no
  "upload a file" button here — open `db/schema.sql` in your editor, select
  all, copy, and paste the whole thing into the SQL editor's text box, then
  click **Run**. That's genuinely it; the editor just executes whatever text
  is pasted in, same as if you'd typed it.
- A GUI client (TablePlus, DBeaver, Postico) if you already use one — these
  usually do have a proper "run script from file" option, unlike the
  browser editors.

Confirm both tables exist before moving on — `\dt` in `psql`, or just look in
the provider's table browser.

### 3. Attach it from DuckDB

This is the exact pattern from Tuesday's demo, now against your own database
instead of the instructor's. From a Python shell, a `.py` script, or
DuckDB's CLI, inside your Codespace:

```python
import duckdb

con = duckdb.connect()
con.sql("INSTALL postgres; LOAD postgres;")
con.sql("""
    ATTACH '**Write your actual connection string here**'
    AS pg (TYPE postgres)
""")
print(con.sql("SELECT table_name FROM information_schema.tables "
              "WHERE table_schema = 'public'").df())
```

Or the same thing directly in SQL, if you're using DuckDB's CLI:

```sql
INSTALL postgres;
LOAD postgres;
ATTACH '**Write your actual connection string here**' AS pg (TYPE postgres);
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

You should see `raw__weather` and `raw__elpris` come back. If they don't —
stop and fix it today, not tomorrow at the table. Common causes: a stray
space or quote in the copied connection string, or `sslmode=require` missing
(both Neon and Supabase require SSL by default).

**Store the connection string in `.env`, not in code.** Copy
`.env.example` from the starter repo to `.env`, paste your connection string
into `DATABASE_URL`. `.env` is already gitignored in the starter repo — check
it hasn't accidentally been committed if you're not sure.

## Optional

If you have time left: look at what your team's two APIs actually return.

```bash
curl "https://www.elprisetjustnu.se/api/v1/prices/2026/08-27_SE3.json"
```

(swap `SE3` for your team's assigned area). And for SMHI, try to find a suitable
station by replacing "Luleå" here:

```bash
curl -s "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station.json" | jq '.station[] | select(.name | test("Luleå"; "i")) | {id, name, latitude, longitude, active}'
```

## We'll follow up

Nothing to hand in. Thursday assumes every team member arrives
with their own working Neon/Supabase project and a successful `ATTACH`.
