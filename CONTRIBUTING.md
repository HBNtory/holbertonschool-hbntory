# Contributing to HBNtory

This guide describes how we work on this project. For the reasoning behind
these choices, see docs/adr/ADR-001-github-workflow.md.

## Language
Everything is written in English: issues, branches, commits, pull requests
and documentation.

## Branches
Two long-lived branches:
- `main` — stable, updated from `dev` at stabilization points
- `dev` — integration branch; all new work starts here

Create every branch from `dev`, one branch per ticket, named `type/description`:

```bash
git switch dev
git pull
git switch -c build/set-up-flask-app
```

Common prefixes: `build/`, `feat/`, `fix/`, `docs/`.

## Commits
Write clear, meaningful commit messages (see naming guide in ADR-001).
Keep commits focused: one logical change per commit.

## Issues
Open issues through the templates only (User Story, Technical, Bug).
Blank issues are disabled — pick the template that fits.

## Pull requests
- One pull request per ticket.
- Target `dev`, not `master`.
- Link the ticket with `Closes #<issue-number>` so it closes automatically
  on merge.
- Fill in the PR description: what, why, changes, how to test.
- Add a screenshot when it helps reviewers (e.g. a running container).
- At least one review is required before merging.

## Before opening a PR
- Run pycodestyle and fix reported issues:
```bash
docker compose exec backoffice pycodestyle app/ main.py
```
- Make sure the app still starts: `docker compose up --build`
## Code conventions

### Style
- Python 3.12.
- All code must pass pycodestyle with no error before a PR is opened.
- Docstrings on every module, class, function and method,
  kept consistent across the project.
