# Friday 4/9: Close out the week

Project work. One deadline for own-data teams, one checkpoint for everyone
else.

## Own-data teams — deadline today

**A loadable base model and its training history must be in your repo by end
of day.**

This is the milestone that was set when your dataset was approved, and it is
deliberately early. It exists so that if your data source turns out not to
work, you find out now.

"Loadable" means someone else can clone the repo, run one command, and get a
model object back. Not a notebook that produced a model once on your laptop.

If you are not going to make it, say so today rather than Tuesday next week. 
That is a normal conversation and an early one is much better than a late one.

## Everyone — the Thursday work should actually be merged

Thursday's exercise produced a new scheduled workflow, among other things. 
Loose ends from an exercise have a way of living on a branch until
they are forgotten.

Before you stop today:

- The PR is merged, not open.
- The scheduled workflow has run at least once for real — triggered by hand
  through `workflow_dispatch` counts.
- The one sentence of reasoning behind your validation rule is written down in
  `docs/`. One sentence. 

## Where you should be

End of week 4, roughly:

- **Component A** ingests from both sources into raw tables, on a schedule,
  and can be run twice without duplicating anything.
- **Sprint 1's backlog** has been refined to reflect more accurately what you
need to do next week.
- Somebody on the team can explain what your validation check does and why
  that particular one.

If component A is not there yet, that's the thing to spend today on.

## Next week

Tuesday 8/9 is cloud platforms, Docker in depth, and Kubernetes conceptually.
Monday's self-study has a short piece of preparation for it — the only reading
task in the next few weeks.
