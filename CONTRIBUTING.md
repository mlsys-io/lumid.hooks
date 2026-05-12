# Contributing to lumid.hooks

## Setup

```bash
pip install uv
uv sync --group dev
uv run pre-commit install --install-hooks -t pre-commit -t prepare-commit-msg -t commit-msg
```

## Before every commit

```bash
uv run pre-commit run --all-files
```

This runs gitleaks, isort, black, ruff, codespell, and mypy. Fix
pre-existing failures rather than suppressing — do not bypass with
`--no-verify` unless explicitly authorized.

## Tests

```bash
uv run pytest -q
```

## Pull Requests

PR title format: `type: description` (optional `[BREAKING]` prefix for
breaking changes). Allowed types: `feat, fix, refactor, chore, test, perf,
docs`. Enforced by `scripts/ci/check_pr_title.py`.

Sign off every commit under the Developer Certificate of Origin
(`git commit -s`, or rely on the `prepare-commit-msg` hook installed above
to append it automatically).

Disclose AI assistance via a commit trailer:
`Co-Authored-By: <agent name> <email>`.

Avoid `--amend` on pushed commits; create a new commit instead. When a
pre-commit hook fails, the commit didn't happen — fix and re-stage, then
commit fresh.

## Release

See [`docs/RELEASE.md`](docs/RELEASE.md) for the version bump, TestPyPI
rehearsal, and PyPI Trusted Publishing workflow.
