make ruff
	uv run ruff check --fix src tests
	uv run ruff format src tests
