Kairix-Mem – Revised System Architecture & Execution Plan

1. Overview

Kairix-Mem is a tiered personal memory system designed for LLM-driven applications. It addresses the limitations of typical session-bound context windows by providing:
	•	Persistent, identity-based memory that spans multiple sessions
	•	Offline reflection to distill long-form conversation logs into human- and machine-readable artifacts
	•	Semantic embeddings for dynamic retrieval of relevant context
	•	A path to deeper assimilation (LoRA or advanced model finetuning) as a future extension

This revised design merges the initial concepts from Claude’s original plan with the MVP-first, fail-fast feedback loop we’ve developed.

⸻

2. Problem Statement

Modern LLMs (e.g., ChatGPT) maintain ephemeral context within a single session but lose continuity across sessions. Users lack a transparent memory model—they can’t see which aspects of previous conversations persist or how. Kairix-Mem offers:
	1.	Personal Identity – A user can cultivate an AI “mind” that evolves over time.
	2.	Reflective Summaries – Offline agent processes logs to create theme-based summaries.
	3.	Context Assembly – Embeddings + scoring inject relevant memories into new user queries.
	4.	Clear Observability – Users can view and edit the system’s memory.

By tackling these four pillars, Kairix-Mem aims to create a trusted AI collaborator rather than a black box.

⸻

3. High-Level Architecture

┌────────────────────────────────────────────────────────┐
│                   Client Applications                 │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                Integration Interfaces (LiteLLM etc.)  │
│  ┌─────────────┐   ┌───────────────┐   ┌────────────┐ │
│  │ Direct Plugin│   │ MCP Server   │   │  (future)  │ │
│  └─────────────┘   └───────────────┘   └────────────┘ │
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│                    Core Components                     │
│  ┌──────────────────┐  ┌───────────────────┐           │
│  │  Memory Storage  │  │Reflection Agent   │  ┌───────┐│
│  │  (SQL + Embeds)  │  │(offline summar.)  │  │Context││
│  └──────────────────┘  └───────────────────┘  │Builder││
│                  ┌────────────────────────────┴───────┘│
│                  │ In-memory embed store + rank        │
└───────────────────▼─────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                 User-Facing Interfaces                 │
│  ┌──────────────────────┐  ┌───────────────────────────┐│
│  │   Chat / CLI UI      │  │ Memory Dashboard (Admin)  ││
│  └──────────────────────┘  └───────────────────────────┘│
└────────────────────────────────────────────────────────┘

	1.	Memory Storage: SQL-based event store for all user messages, plus an in-memory or minimal vector DB for semantic embeddings.
	2.	Reflection Agent: Periodically or manually processes logs, generating four .md files: insights, themes, events, internal_narrative.
	3.	Context Builder: Fetches relevant embeddings, merges them with the user’s new query to produce a final prompt.
	4.	User Interfaces: A CLI or minimal web UI for chat, plus a read-only (or partially editable) memory dashboard.

LoRA training, advanced tier migration, and other enhancements remain future scope.

⸻

4. Phase 1 – MVP Scope

We aim to ship a minimal, fully functional memory system in ~2–3 weeks that demonstrates:
	1.	Persistent Storage (SQL) for user messages
	2.	Offline Reflection for generating .md memory docs
	3.	Embedding Store (in-memory) for quick semantic retrieval
	4.	Context Assembly logic for forging a final prompt
	5.	CLI + Basic Dashboard to show the memory in action
	6.	Fail-fast dev approach + TDD best practices

4.1 Deliverables
	•	SQL DB with schema, migrations, tests
	•	Reflection agent producing 4 doc types
	•	Embedding store for summary docs
	•	Context Assembler that queries top-k relevant summaries
	•	CLI Chat that injects memory context
	•	Memory Dashboard for read-only doc inspection
	•	Full test coverage, typed code, docstrings

4.2 Tech & Tools
	•	Python 3.10+ (strict typing, TDD, fail-fast)
	•	uv for environment and script mgmt
	•	pytest + coverage for tests
	•	mypy --strict enforced
	•	black + isort + pre-commit hooks

⸻

5. Component Detail

5.1 Memory Storage (SQL)
	•	Schema: messages table with [id UUID, user_id TEXT, timestamp, content TEXT, tags TEXT?]
	•	Additional tables or columns if needed (e.g., reflection logs).
	•	Exposed via a simple Python MessageStore class.
	•	TDD approach ensures every method has coverage.

5.2 Reflection Agent
	•	Offline process that scans new messages since last reflection.
	•	Summarizes them into multiple .md files:
	•	insights.md – Key user attributes, knowledge gleaned
	•	themes.md – Recurring topics or emotional undertones
	•	events.md – Big decisions, new facts, timeline
	•	internal_narrative.md – Agent’s perspective, general context
	•	Summaries are stored in plain text plus optional metadata.
	•	Next run includes prior reflection outputs as input to accumulate knowledge.

5.3 Embedding Store
	•	Minimal structure: an in-memory dictionary keyed by doc ID (or filename) with vector embeddings.
	•	Basic similarity search for retrieving top-k docs given a query embedding.
	•	Extensible to a real vector DB in future.

5.4 Context Assembler
	•	For each user query, fetch top-k relevant reflection docs from the embedding store.
	•	Compose them into a final prompt with the new query appended.
	•	This can be a single function or a small pipeline module.

5.5 User Interfaces
	1.	CLI Chat
	•	Read user input, pass to LLM with assembled context.
	•	Show the user which memory fragments were injected.
	2.	Memory Dashboard
	•	CLI or minimal web UI that displays reflection docs.
	•	Possibly filter by date, doc type, or relevance.
	•	Future expansions: editing or tagging memory.

⸻

6. Development Workflow
	1.	Issue-Driven: All tasks broken into GitHub Issues ≤4 hours each.
	2.	Pair Programming with Claude: The CLAUDE.md spells out rules:
	•	TDD, typed code, docstrings mandatory.
	•	No fallback or guess behavior.
	3.	Test-Driven: Must write minimal failing test before writing code.
	4.	Pre-commit Checks: scripts/precheck.sh ensures black, isort, mypy, and pytest all pass.
	5.	Pull Requests: Must reference the relevant issue. All code must be tested and typed.

⸻

7. Future Phases
	•	Phase 2 – Advanced Memory: Concept compaction, multi-tier memory logic, expanded integration (MCP server), memory analytics.
	•	Phase 3 – LoRA Pipeline: Identify training candidates from reflection docs, train miniature LoRAs for domain adaptation.
	•	Beyond: Possibly multi-user synergy, robust security layers, integrated developer tooling.

⸻

8. Conclusion

Kairix-Mem’s MVP focuses on building a stable, easily testable memory system that fosters user trust through transparency and continuity. By layering offline reflection, semantic retrieval, and a well-structured codebase, we pave the way for advanced memory models without losing sight of immediate user value.

This doc consolidates Claude’s original vision, dev guide constraints, and the MVP plan. It should serve as the single source of truth for team alignment.

Let’s build Kairix-Mem—redefining how LLMs remember.