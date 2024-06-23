generate_e2e_test:
	@echo "Generating E2E test file from $(spec_file)..."
	./.venv/bin/python ai_e2e_tests_generator.py "$(spec_file)"

run_tests:
	@echo "Running E2E tests..."
	pytest generated_e2e_tests/