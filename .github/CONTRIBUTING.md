# Contributing to aiogram-dialog-i18n

Thank you for your interest in contributing!
This guide covers everything you need to get started — from setting up the environment to opening a pull request.

## Development setup

```bash
git clone https://github.com/m-xim/aiogram-dialog-i18n.git
cd aiogram-dialog-i18n
uv sync --upgrade
```

## Before committing

Run the full check suite before every commit:

```bash
uv run ruff format
uv run ruff check --fix
uv run ty check
uv run pytest
```

All checks must pass. PRs with failing CI will not be reviewed.

## Branch naming

Use the same type prefix as your commit message:

```
feat/add-lazy-keys
fix/preview-params
docs/update-readme
test/locale-edge-cases
```

## Commit message format

We follow [Conventional Commits](https://www.conventionalcommits.org/). Releases are made from them by
[python-semantic-release](https://python-semantic-release.readthedocs.io/): a commit that is not `feat` or `fix`
(or a breaking change) does not create a new version.

Format: `type(scope): description`

**Types:**
- `feat` — new feature (minor version)
- `fix` — bug fix (patch version)
- `docs` — documentation changes
- `test` — test additions or changes
- `refactor` — code refactoring without behavior change
- `perf` — performance improvements
- `chore` — dependencies, config, tooling

**Rules:**
- Lowercase after the type prefix
- Imperative mood: `add`, `fix`, `update` — not `added`, `fixed`, `updating`
- No period at the end
- Keep the subject line under 72 characters
- Breaking changes: `!` after the type (`feat!: ...`) or a `BREAKING CHANGE:` footer

**Examples:**
```
feat: support LazyProxy as a key
fix: show params in preview
docs: describe locale override
test: cover preview mode
```

## Pull requests

1. Fork the repo and create a branch from `develop` (not `main`).
2. Keep PRs focused — one feature or fix per PR.
3. Add or update tests for every behavior change.
4. Update the README if the public API or behavior changes.
5. Fill in the PR description: what changed and why.

## Reporting issues

Before opening an issue, search [existing issues](https://github.com/m-xim/aiogram-dialog-i18n/issues) to avoid duplicates.

Include:
- Python version and OS
- `aiogram-dialog-i18n`, `aiogram-dialog` and `aiogram-i18n` or `fluentogram` versions
- Minimal reproducible example
- Full traceback if applicable
