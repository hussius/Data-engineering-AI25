# Tuesday Afternoon: Create Your Team Repo

Right after teams and stations are announced. Takes about ten minutes, done
once per team — not something everyone repeats individually.

## Who does this

**One person per team, any volunteer.** Whoever does it becomes the repo's
initial owner/admin, but that doesn't matter much in practice: you're about
to add your whole team and me as collaborators, so nobody depends on one
person's laptop or availability for the rest of the project.

## Steps

1. Go to `github.com/ithogskolan-aim25/aim25-starter`.
2. Click the green **Use this template** button (top right, next to Code) →
   **Create a new repository**.

   **Not "Fork."** Fork keeps a visible link back to the original and GitHub
   will nag you to "sync upstream" — you don't want that. "Use this
   template" gives you a clean, independent repo with the starter files and
   no shared history.

3. **Owner:** pick `ithogskolan-aim25` from the dropdown, not your personal
   account. If the org doesn't show up as an option, stop and message me —
   don't create it under your own username and move on, it's a pain to fix
   later.
4. **Name:** `team-XX`, using your team number from today's board (e.g.
   `team-03`). Keep it consistent — it's how I'll find your repo later.
5. **Public**, then **Create repository**.

## Add your team

Settings (in your new repo) → **Collaborators and teams** → **Add people**.
Add every teammate by their GitHub username, and add me too:

- My username: **hussius**

Since you're an org member, this should grant access immediately — no
invite-acceptance step needed on either side.

## Set branch protection

Settings → **Branches** → **Add branch protection rule**, branch name
pattern `main`:

- ✓ Require a pull request before merging
- ✓ Require approvals: 1

Same rule you already set up for `de-git-ovning` in Week 2 — and this time
it's not optional practice, it's Component F of the project brief.

## Done means

- Repo exists under `ithogskolan-aim25`, named `team-XX`.
- Every teammate and I are listed as collaborators.
- Branch protection is on for `main`.
- The repo URL is posted somewhere your team can find it again (pin it on
  your GitHub Projects board, or drop it in your team's channel).

Wednesday's self-study assumes this repo — and its `db/schema.sql` — already
exists, so it needs to happen today, not "sometime this week."
