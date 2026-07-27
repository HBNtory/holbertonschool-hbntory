# ADR-001: GitHub-based project workflow

## Status
Accepted

## Context
We are a team of several developers, some still learning, working on the same
project. We need a single place to share code, split work into tasks, and keep
documentation, so progress stays visible to the whole team and to the evaluator.
We also need a consistent way to handle branches, reviews and commits, so
contributions stay readable across the team.

## Decision
We use GitHub (organization + Projects) to centralize code, issue tracking and
documentation in one place.

- **Issues**: three deliberately simple ticket types — User Story, Technical,
  Bug — defined as YAML issue forms. Epic and Spike were dropped as unnecessary
  for a project of this size.
- **Branching**: two long-lived branches, `main` and `dev`. Every new branch is
  created from `dev`, follows a `type/description` convention (e.g.
  `build/set-up-flask-app`), and maps to a single ticket.
- **Reviews**: one pull request per ticket, reviewed before it is merged into
  `dev`. `main` is updated from `dev` at stabilization points.
- **Commits**: naming convention based on standard Git good practices.
- **Language**: all issues, pull requests, commits and documentation are written
  in English.

Detailed conventions (branch naming, commit format, PR checklist) live in
CONTRIBUTING.md; this ADR records the decisions, not the step-by-step usage.

## Consequences
Positive:
- Code, tasks and documentation are in one place, easy to share and to review.
- Work is traceable ticket by ticket, which helps both the team and the evaluator.
- Simple ticket types keep the barrier low for team members still learning.

Negative / trade-offs:
- GitHub Projects and issue types have a learning curve for the team.
- The workflow requires discipline: one branch per ticket, PRs kept up to date,
  reviews before merge.
- `Closes #<issue>` is not always added to PRs, so some issues do not close
  automatically and must be closed by hand. To revisit if it becomes a burden.