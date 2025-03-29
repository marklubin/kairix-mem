#!/bin/bash

set -e

echo "🔍 Running Black formatting check..."
black . --check --diff || { echo "❌ Black failed."; exit 1; }

echo "📦 Running isort check..."
isort . --check-only || { echo "❌ isort failed."; exit 1; }

echo "🧠 Running mypy for type checking..."
mypy --strict src/ || { echo "❌ Mypy type check failed."; exit 1; }

echo "✅ Running pytest with coverage..."
pytest --cov=src --cov-report=term-missing || { echo "❌ Tests failed or coverage too low."; exit 1; }

echo "🚀 All pre-submit checks passed!"
