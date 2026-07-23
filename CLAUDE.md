# Claude instructions

## Checks
Run all checks (lint, types, tests, migrations) inside Docker using the commands from the [Makefile](./Makefile), e.g. `docker exec pro-plan-api make cf`.

Never run these tools directly on the host (e.g. `uv run pytest`, `uv run ruff`) — the database and environment are only available inside the `pro-plan-api` container.
