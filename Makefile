.PHONY: format regression_test

format:
	python -m black .

lint:
	python -m mypy dqmj1_info
	python -m ruff check dqmj1_info

regression_test:
	python -m pytest regression_tests/test_*.py