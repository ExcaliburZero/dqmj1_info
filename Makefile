.PHONY = format

format:
	python -m black dqmj1_info/*.py

lint:
	python -m mypy dqmj1_info