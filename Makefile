.PHONY: install test lint build publish clean

install:
	pip install -e .

test:
	pytest tests/ -v

lint:
	black openrouter_fallback/
	ruff check openrouter_fallback/ --fix

build:
	python -m build

publish: build
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
