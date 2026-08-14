.PHONY: help test lint docs deploy clean

help:
	@echo "ACID - Autonomous Computational Intelligence Discovery"
	@echo ""
	@echo "Commands:"
	@echo "  make test     - Run all tests"
	@echo "  make lint     - Lint code"
	@echo "  make docs     - Build documentation"
	@echo "  make deploy   - Deploy UI + API"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make solve    - Solve a problem"
	@echo "  make bench    - Run benchmark"
	@echo "  make batch    - Run batch processing"

test:
	python test_suite.py
	python integration_test.py
	python -c "from acid.testing import run_all_tests; run_all_tests()"

lint:
	pip install flake8
	flake8 acid/ --max-line-length=120 --ignore=E501,W503,E203

docs:
	@echo "Documentation available at:"
	@echo "  - docs/index.html"
	@echo "  - API_DOCS.md"
	@echo "  - SYSTEM_DESIGN.md"

deploy:
	@echo "Deploying ACID..."
	@echo "  UI: https://acid-ui.pages.dev"
	@echo "  API: https://acid-api.rabotatony.workers.dev"

clean:
	rm -rf __pycache__
	rm -rf acid/__pycache__
	rm -rf output/*.json

solve:
	python acid_cli.py solve "Sum of 3 integers" --inputs "[1,2,3]" --expected "[6]"

bench:
	python acid_cli.py bench

batch:
	python batch_process.py
