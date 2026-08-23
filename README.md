# Template repository

This is a template repository that can be used for starting other repositories.

## Validation stack

This template comes with a fully configured validation stack covering static analysis, testing, runtime data validation, and git hook automation.

| Tool | Description |
|---|---|
| **Ruff** | Handles formatting, linting, import sorting, and annotation coverage enforcement in a single tool, replacing Black, Flake8, and isort. |
| **Docstring-tailor** | Performs automatic formatting (line wrapping) for docstrings. |
| **ty** | Static type checker that verifies types flow correctly through the codebase, replacing Mypy. |
| **pytest** | Runs the test suite with branch-level coverage measurement via pytest-cov. |
| **Pydantic** | Enforces the shape and type of data at runtime boundaries. |
| **prek** | Rust-based replacement for pre-commit that runs hooks in parallel before every commit, significantly faster than pre-commit. |

## Makefile

The Makefile orchestrates the validation stack with the following commands, all
run via `uv` for consistent environment management:

| Command | Description |
|---|---|
| `make ruff` | Runs Ruff linting with auto-fix, then formats the codebase. |
| `make format-docstrings` | Applies `docstring-tailor` to all python modules |
| `make ty` | Runs ty for static type checking. |
| `make pytest` | Runs the full test suite with verbose output and branch coverage. |
| `make clean` | Removes caches and temporary files (`__pycache__`, `.ruff_cache`, `.ty_cache`, `.pytest_cache`, `.coverage`, `artifacts`). |
| `make git` | Stages all changes, commits with the default message `"Updated"`, and pushes to remote. |
| `make all` | Runs the full workflow: `ruff` → `docstring-tailor` → `ty` → `pytest` → `clean` → `git`. |