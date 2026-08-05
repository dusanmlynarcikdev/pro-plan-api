# --- docker ---

# show api token
at:
	@cat /data/api-token && echo

# enter api container
c:
	docker exec -it pro-plan-api /bin/bash

# run containers
r:
	docker compose --env-file .env.local up -d

# --- database migrations ---

# run migrations
m:
	alembic upgrade head

# generate migration from diff
mg:
	alembic revision -m "autogenerate" --autogenerate

# rollback last migration
mr:
	alembic downgrade -1

# --- checks ---

# all checks & fixes
cf: lf ty s t

# lint check
l:
	ruff check && ruff format --check

# lint fix
lf:
	ruff format && ruff check --fix

# check database schema
s:
	alembic check

# run tests
t:
	pytest tests -v

# check types
ty:
	ty check
