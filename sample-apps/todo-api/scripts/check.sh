#!/bin/bash
# Script to run tests, type checking, and linting for todo-api

set -e  # Exit on any error

# Activate virtual environment
source .venv/bin/activate

echo "🔍 Running Black formatting check..."
black . --check || { echo "❌ Black failed."; exit 1; }

echo "📦 Running isort check..."
isort . --check-only || { echo "❌ isort failed."; exit 1; }

echo "🧠 Running mypy for type checking..."
mypy --strict src/todo_api/ || { echo "❌ Mypy type check failed."; exit 1; }

echo "✅ Running pytest with coverage..."
pytest tests/ --cov=todo_api --cov-report=term-missing || { echo "❌ Tests failed."; exit 1; }

echo "🎉 All checks passed!"