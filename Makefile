# Makefile for Unified Media Converter v7

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
PYINSTALLER := pyinstaller
SRC_DIR := src
TEST_DIR := tests
DIST_DIR := dist
BUILD_DIR := build

# Default target
.PHONY: help
help:
	@echo "Unified Media Converter - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  help          - Show this help message"
	@echo "  install       - Install dependencies"
	@echo "  test          - Run unit tests"
	@echo "  test-verbose  - Run unit tests with verbose output"
	@echo "  lint          - Run code linter"
	@echo "  format        - Format code with auto-formatter"
	@echo "  run           - Run the application"
	@echo "  build         - Build standalone executable"
	@echo "  clean         - Clean build artifacts"
	@echo "  dist-clean    - Clean all generated files"
	@echo "  docs          - Generate documentation"
	@echo "  package       - Create distributable package"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Run unit tests
.PHONY: test
test:
	$(PYTEST) $(TEST_DIR)

# Run unit tests with verbose output
.PHONY: test-verbose
test-verbose:
	$(PYTEST) --verbose $(TEST_DIR)

# Run code linter
.PHONY: lint
lint:
	flake8 $(SRC_DIR) $(TEST_DIR)
	black --check $(SRC_DIR) $(TEST_DIR)

# Format code
.PHONY: format
format:
	black $(SRC_DIR) $(TEST_DIR)

# Run the application
.PHONY: run
run:
	$(PYTHON) -m $(SRC_DIR).unified_media_converter

# Build standalone executable
.PHONY: build
build:
	$(PYINSTALLER) --onefile --windowed --name unified_media_converter $(SRC_DIR)/unified_media_converter_v_7.py

# Clean build artifacts
.PHONY: clean
clean:
	rm -rf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Clean all generated files
.PHONY: dist-clean
dist-clean: clean
	rm -rf *.spec
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov

# Generate documentation
.PHONY: docs
docs:
	@echo "Generating documentation..."
	@echo "Documentation generation not yet implemented."

# Create distributable package
.PHONY: package
package:
	$(PYTHON) setup.py sdist bdist_wheel

# Install development dependencies
.PHONY: dev-install
dev-install:
	$(PIP) install -e .
	$(PIP) install pytest black flake8

# Run all checks
.PHONY: check
check: lint test
	@echo "All checks passed!"

# Create distribution
.PHONY: dist
dist: clean package
	@echo "Distribution created in dist/"

# Upload to PyPI (requires twine)
.PHONY: upload
upload:
	twine upload dist/*

# Install in development mode
.PHONY: develop
develop:
	$(PIP) install -e .

# Run with profiling
.PHONY: profile
profile:
	$(PYTHON) -m cProfile -o profile.out $(SRC_DIR)/unified_media_converter.py

# Show profiling results
.PHONY: profile-show
profile-show:
	$(PYTHON) -m pstats profile.out

# Create virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv venv
	./venv/bin/pip install --upgrade pip

# Activate virtual environment (Unix/Linux/macOS)
.PHONY: activate
activate:
	@echo "source venv/bin/activate"

# Activate virtual environment (Windows)
.PHONY: activate-win
activate-win:
	@echo "venv\Scripts\activate.bat"
