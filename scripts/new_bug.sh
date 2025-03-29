#!/bin/bash

read -p "Bug title: " TITLE
read -p "Steps to reproduce: " STEPS
read -p "Expected behavior: " EXPECTED
read -p "Actual behavior: " ACTUAL

BODY="### Steps to Reproduce
$STEPS

### Expected
$EXPECTED

### Actual
$ACTUAL"

gh issue create \
  --title "$TITLE" \
  --body "$BODY" \
  --label bug \
  --assignee @me
