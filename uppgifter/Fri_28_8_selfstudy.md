# Friday Self-Study: Finish the Sprint 1 Backlog and Project Plan

Between Thursday's pipeline build and next Tuesday, when Week 4 opens.

This should be team-coordinated; doesn't have to be synchronous —
but someone should own pulling it together.

## Deadline

**Today, Friday 28/8.** 

## What "done" means

Two things, both reflecting your actual team rather than a
template:

### 1. Written Definition of Done

If you wrote one Tuesday afternoon, revisit it now that you've actually
built something (Thursday's pipeline) against it. Does it still hold? A
Definition of Done that survives contact with real work is worth more than
one written in the abstract on day one. One sentence is enough — the
question it has to answer is: *when is a card allowed to move to Done?*

### 2. Sprint 1 backlog on your GitHub Projects board

Not invented example cards — your team's real next three weeks. At minimum,
your backlog should include the work Thursday's session didn't finish:

- Validate raw data before insert (rimlighetskontroller, saknade värden,
  dubbletter — Component A explicitly requires this, and today's pipeline
  almost certainly doesn't do it yet).
- Schedule the feature pipeline to run daily, unattended (Component A: "utan
  att någon startar den manuellt").
- Design and build your features table — what a feature *row* looks like for
  your team's target, joining weather and price data in time.
- Start the training pipeline (Component B): read features from Postgres,
  retrain `train.py`'s model, register a version.

Move cards to the columns that reflect where things actually stand — some of
this may already be in progress from Thursday, not all of it starts in
Backlog.

## Why this matters more than it looks

On 17/9 — you'll be presenting your project plan and how you're working agilely, 
not just demoing the system. 

## Deliverable

Your team's Sprint 1 backlog and Definition of Done, visible on your GitHub
Projects board, plus a short project plan document (a few paragraphs is
enough — decomposition, sequencing, scoping, as covered in Week 2's agile
intro) committed to your repo. Due today, 28/8.

## We'll follow up

Tuesday 1/9 opens with a quick round: one thing your team scoped *out* of
Sprint 1 on purpose, and why. Bring that answer.
