.PHONY: format lint regression_test compile_executables

format:
	python -m black .

lint:
	python -m mypy .
	python -m ruff check .

regression_test:
	python -m pytest regression_tests/test_*.py

compile_executables:
	pyinstaller extract_dqmj1_files.py --add-data "dqmj1_info/data:dqmj1_info/data" --noconfirm