# all checks & fixes
cf: lf ty t

# lint
l:
	ruff check && ruff format --check

# lint fix
lf:
	ruff check --fix && ruff format

# run database migrations
mu:
	alembic upgrade head

# generate database migrations
mg:
	alembic revision -m "autogenerate" --autogenerate

# types
ty:
	ty check

# tests
t:
	pytest tests -v
