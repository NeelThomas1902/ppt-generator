.PHONY: test test-unit test-api test-integration test-coverage test-fast

# Run the complete test suite
test:
	pytest -v

# Unit tests only (validators and utility helpers)
test-unit:
	pytest tests/test_services.py -v

# API endpoint smoke tests
test-api:
	pytest tests/test_api.py -v

# Integration / end-to-end workflow tests
test-integration:
	pytest tests/test_integration.py -v

# Run tests and generate an HTML coverage report in htmlcov/
test-coverage:
	pytest --cov=app --cov-report=term-missing --cov-report=html -v

# Stop on the first failing test (fast feedback)
test-fast:
	pytest -x -v
