.PHONY = format

format:
	python -m black .

lint:
	python -m mypy dqmj1_info