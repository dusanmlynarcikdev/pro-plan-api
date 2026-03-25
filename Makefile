# all checks & fixes
cf: lf ty t

# lint
l:
	ruff check && ruff format --check

# lint fix
lf:
	ruff check --fix && ruff format

# types
ty:
	ty check

# tests
t:
	pytest tests -v -s
