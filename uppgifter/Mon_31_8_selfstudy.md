# Monday Self-Study: Know Your Baseline Before Sprint 1 Starts

Between Week 3 wrapping up and Week 4 opening — no lecture today, but
Tuesday's session assumes you've done this.

**Deadline: today, Monday 31/8**, before Tuesday's 13:00 sprint planning.

## Why this matters more than a normal "read the code" task

Tuesday opens with Spark/Databricks in the morning, then **Sprint 1
planning at 13:00** — where your team commits to what you're actually
building over the next two weeks, including the start of your training
pipeline (Component B). That backlog should be grounded in what's
genuinely wrong with the baseline model you're inheriting, not guessed at
in the room. Today's job is to know that, individually, before you sit down
as a team.


## What to do

### 1. Read `model/train.py` (15–20 min)

Be sure to read the function docstrings as well as the code!

- **`load_prices` / `load_weather`** — two different timestamp conventions
  from two different sources, and what happens if you get either wrong.
- **`daily_price_table`** — why "24 rows per day" is not a safe assumption
  (Sweden switched from hourly to 15-minute prices on 2025-10-01).
- **`build_features`** — the information boundary: what you actually know
  at prediction time vs. what this baseline quietly cheats by using.

Then read the **LIMITATIONS** block at the very bottom, all seven items.


### 2. Run `model/utforskning.ipynb` (15–20 min)

This is the notebook the baseline model was built from — a tour of the
actual problems in the data, not a finished analysis. Before running it,
set `AREA` and `STATION` at the top of the notebook to your team's
assigned price area and SMHI station (from Week 3).

As you run it, look for:

- The prices-per-day plot — the same 24→96 jump `train.py` warned about,
  now visible.
- Negative prices and price spikes — real, not measurement error, and they
  dominate any error metric you'll report.
- The missing-weather-hours check, and the question the notebook asks you
  to actually answer: how big a gap is safe to interpolate, and where's
  your cutoff? Write your answer down somewhere.

If you haven't already, `cp .env.example .env` and fill in `PRICE_AREA` and
`TARGET` first — same setup `train.py` needs.

## Come to Tuesday with

Come to 13:00 sprint planning with **one or two limitations from the list that are
clearly relevant to your team's specific area and target**, ready to turn
into backlog items. If your team has `TARGET=peak`, item #2 (the
resolution change) isn't optional background reading — it's a real bug in
the data you're about to train on.

## We'll follow up

Tuesday's sprint planning is where these become actual tickets. Nobody
should be reading `train.py` for the first time in that room.
