#!/bin/bash
# Script to create a new database migration

set -e  # Exit on any error

# Activate virtual environment
source .venv/bin/activate

# Create the initial migration
alembic revision --autogenerate -m "Initial migration"

echo "🎉 Migration created successfully!"