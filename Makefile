# all checks & fixes
cf: lf ty s t

# show api token
at:
	@cat /data/api-token && echo

# enter docker container
dc:
	docker exec -it pro-plan-api /bin/bash

# lint check
l:
	ruff check && ruff format --check

# lint fix
lf:
	ruff format && ruff check --fix

# run database migrations
m:
	alembic upgrade head

# generate database migration from diff
mg:
	alembic revision -m "autogenerate" --autogenerate

# rollback last database migration
mr:
	alembic downgrade -1

# check database schema
s:
	alembic check

# run tests
t:
	pytest tests -v

# check types
ty:
	ty check
