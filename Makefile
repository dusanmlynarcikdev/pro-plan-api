# all checks & fixes
cf: lf ty s t

# lint check
l:
	ruff check && ruff format --check

# lint fix
lf:
	ruff check --fix && ruff format

# run database migrations
m:
	alembic upgrade head

# generate database migration from diff
mg:
	alembic revision -m "autogenerate" --autogenerate

# check database schema
s:
	alembic check

# run tests
t:
	pytest tests -v

# check types
ty:
	ty check