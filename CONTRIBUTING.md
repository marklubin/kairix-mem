# CONTRIBUTING.md – Developer Onboarding & Standards

Welcome to the Hierarchical Memory System (HMS) project. This document outlines the tools, environment setup, and development conventions to be followed by all contributors.

---

## 🛠️ Python Environment Setup (with `uv` + `venv`)

We use [`uv`](https://github.com/astral-sh/uv) as our primary Python project manager. It's fast, deterministic, and designed for modern workflows—similar to `npm` or `pnpm`, but for Python.

> If you're familiar with Node.js workflows: `uv add` ≈ `npm install`, `uv pip freeze` ≈ `npm shrinkwrap`, and `pyproject.toml` ≈ `package.json`.

We use `uv` as our primary Python project manager and dependency resolver, alongside a standard `venv`-based local environment.

### 📦 Project Bootstrap

```bash
# Clone the repo
$ git clone https://github.com/your-org/kairix-mem
$ cd kairix-mem

# Create and activate a virtual environment
$ uv venv
$ source .venv/bin/activate

# Install all dependencies from pyproject.toml
$ uv pip install
```

> 🚫 Do not use `pip install` directly. All dependency additions must go through `uv add`:
```bash
$ uv add openai typer numpy  # Example of adding packages
```

> 📌 Use `uv pip freeze > requirements.txt` to regenerate pinned output if needed for tooling or CI.
```

> ✅ All team members must work within the `.venv` environment and manage dependencies using `uv`.

---

## 🧪 Testing & TDD Workflow

We follow strict **test-driven development** using Pytest. Every task:

1. Starts by writing a **failing test**
2. Implements **minimal passing code**
3. Refactors with tests still passing

To run tests:

```bash
$ pytest
```

### ✅ Test Standards

- All new code **must** have corresponding unit or integration tests
- Test coverage target is **90%+**
- Use `unittest.mock` or `pytest-mock` for isolation

---

## 🧼 Formatting, Linting, and Type Checking

All code must conform to the following:

- **Black** for formatting
- **isort** for import sorting
- **Mypy** for static type checking (strict mode)
- **Pylint** (optional)

Install tools:

```bash
$ uv pip install black isort mypy pytest
```

Check code:

```bash
$ black .
$ isort .
$ mypy --strict src/
```

> ⚠️ CI will reject code that fails lint/type/style checks

---

## 🧰 Error Handling & Import Standards

### 🔥 Fail Fast Philosophy

This project follows a **fail-fast design philosophy**:
- If required data, configuration, or dependencies are missing, the system **must crash clearly and immediately**.
- Never attempt silent fallbacks or speculative guessing. Misconfigurations should never be "recovered from" at runtime.

### 🚫 Prohibited Patterns
- **No try/except around imports** to bypass missing dependencies.
- **No conditional imports** based on platform or environment—use explicit checks early and crash loud.
- **No runtime guessing** of config defaults unless explicitly specified.

### ✅ Required Patterns
- Never handle or recover from invalid program state. Always `raise` a specific exception subclass.
- Do not guess or infer user or config intent during runtime. If something is missing or ambiguous, fail explicitly.
- Always validate preconditions early in your module or service entry point.
- Raise specific exceptions (e.g., `MissingConfigError`, `UnsupportedProviderError`) instead of vague `Exception`.
- Log error context before raising if it helps debugging, but do not suppress.

### 📦 Import Structure Standards
- All imports must be declared at the **top** of the file.
- Use **absolute imports** throughout.
- Organize imports in this strict order:
  1. Standard library
  2. Third-party packages
  3. Internal app modules (e.g. `from kairix_mem.memory import TierStore`)

Separate each group with a blank line. Use `isort` to enforce this.

> ⚠️ Any attempt to obscure or recover from a broken runtime environment is considered a bug.

---

## 🧬 Typing Requirements

All Python code must use **type annotations** to improve code clarity, tooling support, and reliability. We enforce this via `mypy --strict`.

### 📌 Basic Type Annotation Guide

#### ✅ Function Signatures
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

#### ✅ Variables
```python
name: str = "Alice"
age: int = 42
```

#### ✅ Collections
```python
from typing import List, Dict, Optional

tags: List[str] = ["memory", "reflection"]
settings: Dict[str, int] = {"depth": 3}
maybe_id: Optional[int] = None  # int or None
```

#### ✅ Custom Types
```python
from typing import TypedDict

class MemoryEntry(TypedDict):
    timestamp: str
    content: str
```

#### 🧪 Enforcing Types with `mypy`
Run:
```bash
mypy --strict src/
```
> 🔍 Flags like `--disallow-untyped-defs` and `--warn-unused-ignores` will catch issues early.

> ⚠️ No `# type: ignore` comments allowed unless explicitly justified.

Refer to [https://docs.python.org/3/library/typing.html](https://docs.python.org/3/library/typing.html) for more advanced patterns.

All Python code must be type-annotated.

- No use of `Any` unless absolutely unavoidable
- No `# type: ignore` without prior approval
- Use `typing` module types across all APIs

---

## 📁 Project Layout

```
.
├── src/                  # Main source code
│   ├── memory/           # Core memory logic
│   ├── reflection/       # Reflection agent logic
│   ├── embedding/        # Embedding & search tools
│   └── ui/               # CLI or web UI components
├── tests/                # Unit + integration tests
├── scripts/              # Dev tools & CLI scripts
├── requirements.txt      # Pinned deps (generated by uv freeze)
└── pyproject.toml        # Configs for black, isort, mypy, etc.
```

---

## 🔀 Branch & Commit Policy

We use a conventional branching model:

- `main` → protected release branch
- `dev` → active development branch
- Feature branches: `feature/[task-id]-short-desc`

### 🔖 Commit Format

```
feat: Add embedding store setup (#P1.3.1)
fix: Correct SQL query interface (#P1.1.4)
```

---

## 📦 Building & Packaging

We use `uv` and `pyproject.toml` as the primary dev environment configuration and task runner.

### 💻 Pre-Submission Build Script + Pre-commit Hook

Before submitting any PR, you **must run the following build check script** locally. This ensures that code meets formatting, type, and test coverage standards.

```bash
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

# Optional: Git commit if everything passes
# git commit -m "feat: Your message here (#TASK-ID)"
```

> 🔁 You can add this as `.scripts/precheck.sh` and run via `uv run precheck` (see pyproject section).

### ✅ Pre-commit Hook Integration

To automatically run the build checks before each commit, set up a Git pre-commit hook:

```bash
mkdir -p .git/hooks
cat << 'EOF' > .git/hooks/pre-commit
#!/bin/bash
bash scripts/precheck.sh
EOF
chmod +x .git/hooks/pre-commit
```

This ensures every commit passes `black`, `isort`, `mypy`, and `pytest` before it’s accepted locally.

### ✅ Suggested `pyproject.toml` Configuration

```toml
[project]
name = "kairix-mem"
version = "0.1.0"
description = "Reflective tiered memory for AI systems"
requires-python = ">=3.10"

[tool.uv]
virtualenvs.in-project = true

[tool.black]
line-length = 88

[tool.isort]
profile = "black"

[tool.mypy]
strict = true
ignore_missing_imports = true

[tool.kairix.scripts]
lint = "black . && isort ."
typecheck = "mypy src/"
test = "pytest --cov=src --cov-report=term-missing"
dev = "python src/main.py"
precheck = "bash scripts/precheck.sh"
```

> Run all checks before opening a PR: `uv run precheck`

TBD – future version will include packaging logic via `setuptools` or `hatchling`. For now, focus on source builds and dev workflow.

---

## 📚 Documentation Standards

### 📖 Code Documentation
- Every module, class, function, and method **must include a complete docstring**.
- Use **Google-style** docstrings.
- Include **parameters, return types, exceptions, and usage examples**.
- All complex logic should have **inline comments explaining why**, not just what.
- Public APIs must include **minimal working examples** in docstrings.

### 🔁 Cross-Referencing Third-Party Libraries
- If your implementation uses or wraps a third-party library:
  - Reference the **official documentation URL** in the module or method docstring.
  - Provide **brief explanation** of how/why the library is used.
  - Link to **specific methods, patterns, or examples** if applicable.

### ✅ Verification Before Use
- You **must consult the original source code and documentation** of any third-party library before integrating.
- Confirm behavior, inputs, outputs, and edge cases. Do not rely on ChatGPT or AI summaries alone.
- Incorrect assumptions about libraries are treated as bugs.

> 🔍 Our goal is to ensure that future contributors (and AI agents) can reason through any function with only the source code and its documentation.

---

## 🔁 Commit & PR Submission Process

### 📝 Commit Messages
- Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):
  - `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:` etc.
  - Always include the related issue ID (e.g. `(#P1.1.3)`) in the commit title
- Use the template in `.gitmessage.txt` to guide structure

```txt
feat: Implement SQL insert function (#P1.1.3)

- Added insert_message() to SQL layer
- Wrote corresponding test cases
- Includes logging and type validation
```

### 📦 Opening a Pull Request
- Use the GitHub CLI or web UI:
  ```bash
  gh pr create --fill --base dev --head feature/P1.1.3-sql-insert
  ```
- PRs must reference the corresponding issue number in title or description
- Include:
  - A short summary of the implementation
  - Any decisions, deviations, or assumptions made
  - Screenshots or logs if applicable (e.g. CLI tools, dashboards)

### ✅ Requirements for Merge
- All code must:
  - Pass the full `precheck` script
  - Include required tests + documentation
  - Pass CI/CD
- PRs must be approved by at least one reviewer (human or mentor AI)
- The branch must be up-to-date with `dev`

---

## 🐛 Bug Reporting & Management

All bugs must be tracked and approved through GitHub Issues. **No contributor is allowed to self-assign or resolve a bug without explicit approval.**

### 🔍 When You Discover a Bug:
1. Create a **GitHub Issue** under the `bug` label.
2. Include:
   - Clear title and description
   - Steps to reproduce
   - Expected vs. actual behavior
   - Logs, screenshots, stack trace if applicable
3. Link the bug to any affected feature issue or PR.
4. Do **not** attempt to fix unless the issue is explicitly assigned to you.

### ✅ Requirements for Bug Fixes
- Each bug fix must:
  - Be addressed in its **own PR**
  - Include a regression test
  - Reference the original bug issue ID in the PR and commit

### 🚀 Shortcut Script: `uv run bug`

To quickly create a structured GitHub bug issue from CLI:
```bash
uv run bug
```

This runs the helper script below:

```bash
# scripts/new_bug.sh
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
```

> ⚠️ All contributors must use this process and respect triage decisions.

---

## 🤝 Contribution Notes

- All work begins with an approved GitHub Issue
- PRs must reference the issue ID
- No untested code will be merged
- Ask questions in the issue thread before implementation
- Use Claude or other mentors for pair programming

---

Let’s build something powerful, reusable, and clean. Thanks for contributing! 🙌

