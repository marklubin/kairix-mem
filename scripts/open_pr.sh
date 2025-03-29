#!/bin/bash

# Usage: ./scripts/open_pr.sh feature/P1.3.2-memory-embedding
# Requires GitHub CLI installed and authenticated

BRANCH_NAME=$1

if [ -z "$BRANCH_NAME" ]; then
  echo "Usage: $0 feature/branch-name"
  exit 1
fi

gh pr create --fill --base dev --head "$BRANCH_NAME"
