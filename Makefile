# all checks & fixes
cf: lf ty d t

# lint check
l:
	ruff check && ruff format --check

# lint fix
lf:
	ruff check --fix && ruff format

# check database schema
d:
	alembic check

# run database migrations
m:
	alembic upgrade head

# generate database migration from diff
mg:
	alembic revision -m "autogenerate" --autogenerate

# check types
ty:
	ty check

# run tests
t:
	pytest tests -v
