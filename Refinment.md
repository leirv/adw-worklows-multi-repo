# Pipeline CLI — Contract-Driven Multi-Agent Execution Pipeline

A deterministic CLI tool built on LangGraph that orchestrates Claude (`claude -p`) through a contract-driven, multi-step code generation pipeline.

## Core Concepts

- **Deterministic pipeline** — the graph structure is fixed; Claude handles the intelligence within each node
- **Contract-Driven Design (CDD)** — every node boundary is enforced by a Pydantic contract. If the output doesn't match the contract, it doesn't move forward
- **Prompts as configuration** — each node's behavior is defined in a Markdown file, not hardcoded in Python
- **Human-in-the-loop** — structured approval gates and an "I'm Stuck" escape hatch
- **Full observability** — every execution produces a complete log trail with a unique run ID
- **Checkpointing** — LangGraph checkpointing enables resuming failed runs from where they stopped
- **Git worktree isolation** — each execution runs in an isolated git worktree; code is never written to the working branch

## Architecture Overview

```
CLI (Typer)
  │
  ├── mytool python "..."
  ├── mytool react "..."
  ├── mytool dotnet "..."
  └── mytool terraform "..."
        │
        ▼
  Pipeline Registry → dispatches to the correct composition root
        │
        ▼
  [Subgraph per pipeline] → each pipeline owns its graph, nodes, prompts, contracts
        │
        ▼
  Nodes → Agent (claude -p) | Gate (human) | Tool (deterministic)
```

Each pipeline is its own composition root. Pipelines do not share prompts or contracts. They share only infrastructure (CLI, logging, LLM invocation, base state types).

## Pipeline Flow

```
[Discovery]
     │
  ┌──┴──────┐
  has code   empty directory
  │          │
  ▼          ▼
 [Scan]   [Interview Loop]
  │       (interactive with human)
  │          │
  └────┬─────┘
       ▼
  .pipeline/codebase.md exists
       │
  [Scope Analyzer]
       │
    ┌──┴────────────┬──────────────┐
   GOOD          BROAD/AMBIGUOUS   SMALL
    │                │               │
    │           [Human Scope       [Direct Execute] → END
    │            Gate]             (skip pipeline,
    │                │             just claude -p)
    ▼                ▼
  [Create Worktree]◄─┘
       │
       │  git worktree add .worktrees/<run-id> -b pipeline/<run-id>
       │
  [Architect]                        ── all nodes below operate
       │                                inside the worktree ──
  [Human Approval]
       │
  [Test Writer]
       │
  [Coder] ◄──────────────────┐
       │                      │
  [Validation]                │
       │                      │
    ┌──┴───┐                 │
  pass  fail  stuck           │
    │    └───────────────────┘
    │         │  (max 3 retries)
    │         ▼
    │   [I'm Stuck Agent]
    │         │
    │   human guidance
    │         │
    │   routes back into pipeline
    │
    ▼
  [Create Merge Request]
       │
       │  gh pr create → pipeline/<run-id> → target branch
       │
       ▼
      END (human reviews and merges)
```

### Node Descriptions

| Node | Type | Input | Output | Description |
|------|------|-------|--------|-------------|
| Discovery | Agent (`claude -p`) or Gate | Directory | `.pipeline/codebase.md` | Scans existing code or interviews the human to build project context |
| Scope Analyzer | Agent (`claude -p`) | User prompt + codebase context | Scope classification | Evaluates if the prompt is too broad, too small, ambiguous, or good |
| Human Scope Gate | Gate (`interrupt()`) | Sub-scope options or clarifying questions | Refined prompt | Asks human to narrow down or clarify the requirement |
| Create Worktree | Tool (deterministic) | Run ID + target branch | Worktree path | Creates git branch and worktree for isolated execution |
| Architect | Agent (`claude -p`) | Refined requirement + codebase context | N solution proposals (ADRs) | Analyzes the requirement and generates multiple architecture options |
| Human Approval | Gate (`interrupt()`) | Solution options | Selected ADR | Presents options to the human, pauses until one is selected |
| Test Writer | Agent (`claude -p`) | Approved ADR | Test files | Reads the ADR and generates tests that validate the architecture |
| Coder | Agent (`claude -p`) | ADR + test files | Source code | Writes code that makes the tests pass |
| Validation | Tool (deterministic) | Source code + tests | Pass/Fail | Runs the test suite (e.g., pytest). Routes to retry, end, or stuck |
| I'm Stuck | Agent + Gate | Failure context | Human guidance | Summarizes the failure, asks the human for direction |
| Create MR | Tool (deterministic) | Worktree with committed code | Merge request URL | Commits changes, pushes branch, creates MR with `gh pr create` |

### Node Types

| Type | Autonomous | Example |
|------|------------|---------|
| Agent node | Yes — calls `claude -p` | Architect, Test Writer, Coder |
| Gate node | No — waits for human | Human Approval, I'm Stuck |
| Tool node | Yes — deterministic | Validation (pytest), Lint |

## Discovery Node

The Discovery node runs before anything else and ensures the pipeline has context about the codebase it's working with. It operates in two modes.

### Scan Mode (existing project)

When the target directory contains code, Discovery uses `claude -p` to analyze the repository structure, tech stack, patterns, and conventions. It produces a `.pipeline/codebase.md` file. On subsequent runs, it reads the existing file instead of re-scanning (unless explicitly asked to refresh).

### Interview Mode (greenfield project)

When the target directory is empty, Discovery enters an interactive loop with the human to gather project context. It asks about domain, users, core entities, tech stack, constraints, integrations, and architectural preferences.

The interview is a mini-graph:

```
[Seed Questions]  →  [Follow-up Agent]  →  enough? ── no ──→ [Follow-up Agent] (loop)
 (domain, users,      (reads answers,         │
  entities, stack)     identifies gaps,       yes
                       asks deeper)            │
                                               ▼
                                        [Profile Generator]
                                         produces codebase.md
```

Both modes produce the same output — `.pipeline/codebase.md` — so the rest of the pipeline doesn't care whether it's a greenfield or existing project.

### `.pipeline/codebase.md` example

```markdown
# Codebase Profile

## Type
Greenfield — Python 3.12 (or: Existing monolith — Python 3.12, FastAPI)

## Domain
Internal team productivity — task management for small dev teams

## Core Entities
- Task (title, description, status, assignee, labels, due date)
- Project (name, members, tasks)
- User (name, email, role)

## Stack
- FastAPI, SQLAlchemy 2.0, Pydantic v2, PostgreSQL

## Patterns
- Clean architecture, repository pattern, async throughout

## Conventions
- snake_case, tests mirror src/ structure

## Integrations
- Slack webhooks, GitHub webhooks

## Deployment
- Docker, AWS ECS
```

## Scope Analyzer Node

The Scope Analyzer evaluates whether the user's prompt is appropriately scoped for a single pipeline execution. It classifies the prompt into one of four categories:

| Classification | Action |
|----------------|--------|
| **GOOD** | Proceed to Architect |
| **TOO_BROAD** | Present sub-scopes to human, ask them to pick one |
| **TOO_SMALL** | Skip the full pipeline, execute directly with `claude -p` |
| **AMBIGUOUS** | Ask clarifying questions before proceeding |

Both TOO_BROAD and AMBIGUOUS route through a Human Scope Gate where the user narrows or clarifies the requirement before the pipeline continues.

## Git Worktree Isolation

Every pipeline execution is isolated in a git worktree. The pipeline never writes code to the current working branch.

### Lifecycle

```
1. Pipeline starts
   │
   ▼
2. Create branch: pipeline/<run-id>  (e.g., pipeline/2026-02-11_a3f8c1)
   │
   ▼
3. Create worktree: .worktrees/<run-id>/  → checked out on the new branch
   │
   ▼
4. All nodes (Coder, Test Writer, Validation) operate inside the worktree
   │
   ▼
5. On success → create Merge Request from pipeline/<run-id> → target branch
   │
   ▼
6. Human reviews and merges the MR
   │
   ▼
7. Cleanup: remove worktree
```

### Why worktrees

- **Isolation** — the pipeline can't corrupt the working branch. If it fails, delete the worktree and the branch, nothing is lost.
- **Parallel runs** — multiple pipeline executions can run simultaneously, each in its own worktree, without conflicts.
- **Human review** — the output is a merge request, not direct commits. The human has full control over what gets merged.
- **Diffable** — the MR shows exactly what the pipeline produced, making it easy to review.

### Worktree handling in nodes

The worktree path is part of the run context. Every node that touches the filesystem uses it:

```python
# Coder node runs claude -p with the worktree as working directory
subprocess.run(
    ["claude", "-p", prompt, "--allowedTools", "Write,Edit,Bash"],
    cwd=state["run_ctx"].worktree_path,  # isolated
)

# Validation node runs tests inside the worktree
subprocess.run(
    ["pytest"],
    cwd=state["run_ctx"].worktree_path,  # isolated
)
```

### MR creation

After validation passes, the pipeline commits all changes in the worktree, pushes the branch, and creates a merge request using `gh pr create`. The MR body includes:

- The original requirement
- The selected ADR
- A summary of what was generated
- A link to the run logs

### CLI commands

```bash
mytool python "Build a REST API"              # runs in worktree, creates MR
mytool cleanup <run-id>                        # removes worktree and branch
mytool cleanup --all                           # removes all finished worktrees
```

## Code Constraints

- **No file over 200 lines** — if a file is growing past this, split it. No exceptions.
- **Single Responsibility** — each file, class, and function does one thing. A node file contains node logic. A contract file contains contracts. A prompt file contains a prompt. They don't bleed into each other.
- **No monolithic pipeline files** — the graph wiring, node implementations, contracts, state, and prompts each live in their own file. Never build an entire pipeline in a single file.
- **Keep functions short** — if a function needs a scroll, it's doing too much. Extract.
- **Flat is better than nested** — prefer composition over deep inheritance. Prefer small modules over large ones.

## Three-Layer Architecture

### 1. Prompts (Markdown) — define behavior

Each node's system prompt lives in a `.md` file. The prompt defines the role, behavior, constraints, and expected output format. Changing behavior means editing a Markdown file, not touching code.

### 2. Contracts (Pydantic) — define shape

Every node boundary is enforced by a Pydantic model. The contract validates the output before state is passed downstream. If validation fails, the node retries or escalates.

### 3. Nodes (Python) — define mechanics

The node code reads the prompt file, constructs the full prompt from state, calls `claude -p`, parses the output, validates against the contract, and logs everything. Node code rarely changes.

## Pipelines

Each pipeline is a self-contained composition root targeting a specific domain.

| Pipeline | Focus | Test Runner | Specific Tooling |
|----------|-------|-------------|------------------|
| Python | Python 3.12+, FastAPI, SQLAlchemy | pytest | ruff, black |
| React | React, TypeScript, Vite | vitest / jest | eslint, prettier |
| Dotnet | .NET 8, C#, ASP.NET Core | dotnet test | dotnet build |
| Terraform | Terraform, AWS/Azure/GCP | terraform validate | tflint, checkov |

## Project Structure

```
pipeline-cli/
├── pyproject.toml
├── README.md
├── src/
│   └── pipelines/
│       ├── __init__.py
│       ├── cli.py                      # Typer app — CLI entry point
│       ├── shared/
│       │   ├── llm.py                  # claude -p invocation wrapper
│       │   ├── state.py                # Base state types
│       │   ├── logging.py              # RunContext, NodeLogger
│       │   ├── contracts.py            # Base contract types
│       │   ├── git.py                  # Worktree creation, branch management, MR creation
│       │   └── nodes.py                # Reusable node patterns
│       │
│       ├── python/
│       │   ├── __init__.py
│       │   ├── graph.py                # Composition root — builds the LangGraph
│       │   ├── nodes.py                # Node implementations
│       │   ├── contracts.py            # Pydantic contracts per node boundary
│       │   ├── state.py                # Pipeline-specific state schema
│       │   └── prompts/
│       │       ├── discovery_interview.md
│       │       ├── discovery_followup.md
│       │       ├── scope_analyzer.md
│       │       ├── architect.md
│       │       ├── test_writer.md
│       │       ├── coder.md
│       │       └── im_stuck.md
│       │
│       ├── react/
│       │   ├── (same structure as python/)
│       │   └── prompts/
│       │       └── (react-specific prompts)
│       │
│       ├── dotnet/
│       │   ├── (same structure)
│       │   └── prompts/
│       │
│       └── terraform/
│           ├── (same structure)
│           └── prompts/
│
├── .pipeline/                          # Project context (committed to repo)
│   └── codebase.md                    # Generated by Discovery node
│
├── .runs/                              # Execution logs (gitignored)
│   └── <run-id>/
│       ├── run.json
│       ├── discovery/
│       ├── scope_analyzer/
│       ├── architect/
│       ├── human_approval/
│       ├── test_writer/
│       ├── coder/
│       │   ├── attempt_1/
│       │   └── attempt_2/
│       ├── validation/
│       └── im_stuck/
│
└── tests/
    ├── test_contracts.py
    ├── test_python_graph.py
    └── ...
```

## Observability

Every execution generates a unique run ID and a full log trail.

### Run Directory Structure

Each node logs:
- `input.json` — state received by the node
- `prompt.md` — the actual prompt sent to `claude -p`
- `raw_output.txt` — raw response from Claude
- `output.json` — parsed and validated output
- `contract_validation.json` — pass/fail with error details
- `log.jsonl` — timestamped event stream

Retry-capable nodes (Coder, Validation) log each attempt in separate subdirectories (`attempt_1/`, `attempt_2/`, etc.).

### Run Summary (`run.json`)

Top-level metadata for the entire execution: pipeline, input, status, duration, nodes executed with timing, human interventions, total Claude calls, and whether the stuck agent was triggered.

### CLI Commands

```bash
mytool python "Build a REST API"                # run in worktree, creates MR
mytool logs <run-id>                             # view run summary
mytool logs <run-id> --node coder                # view coder logs
mytool logs <run-id> --node coder --attempt 2    # specific retry
mytool resume <run-id>                           # resume from checkpoint
mytool cleanup <run-id>                          # remove worktree and branch
mytool cleanup --all                             # remove all finished worktrees
```

## Checkpointing

LangGraph checkpointing is enabled to persist graph state after each node completes. This allows:

- **Resume on failure** — if the process crashes or is interrupted, resume from the last completed node
- **Resume after "I'm Stuck"** — human provides guidance asynchronously, then resumes
- **Replay** — re-run from any checkpoint with modified state

---

## Development Phases

### Phase 1 — Foundation

- [ ] Project scaffolding (pyproject.toml, src layout, dependencies)
- [ ] Shared infrastructure: `claude -p` wrapper, RunContext, NodeLogger
- [ ] Base state types and contract base classes
- [ ] Git infrastructure: worktree creation, branch management, MR creation, cleanup
- [ ] CLI skeleton with Typer (command dispatch, `logs`, `resume`, `cleanup`)

### Phase 2 — Discovery and Scope Analysis

- [ ] Discovery node: Scan Mode (analyze existing codebase with `claude -p`)
- [ ] Discovery node: Interview Mode (interactive human loop for greenfield projects)
- [ ] Discovery follow-up agent (identifies gaps, asks deeper questions, loops until sufficient)
- [ ] Profile Generator (produces `.pipeline/codebase.md` from either mode)
- [ ] Scope Analyzer node and contract (`ScopeContract`)
- [ ] Human Scope Gate (narrow down TOO_BROAD, clarify AMBIGUOUS)
- [ ] Direct Execute path for TOO_SMALL prompts
- [ ] Conditional routing: Scope classification → appropriate path

### Phase 3 — Python Pipeline (first composition root)

- [ ] Define contracts: `ArchitectOptionsContract`, `ADRContract`, `TestContract`, `CodeContract`
- [ ] Write prompt files: `architect.md`, `test_writer.md`, `coder.md`, `im_stuck.md`
- [ ] Implement nodes: Architect, Test Writer, Coder, Validation
- [ ] Wire the LangGraph: edges, conditional routing (retry loop, stuck escalation)
- [ ] Human Approval gate with `interrupt()`
- [ ] I'm Stuck agent with `interrupt()`
- [ ] LangGraph checkpointing integration
- [ ] End-to-end test of the full pipeline

### Phase 4 — Observability and CLI Polish

- [ ] Structured logging to `.runs/` directory
- [ ] `mytool logs` command for viewing run history and node details
- [ ] `mytool resume` command for checkpoint-based resumption
- [ ] Progress display during execution (spinner, step counter)
- [ ] Error formatting and user-friendly output

### Phase 5 — Additional Pipelines

- [ ] React pipeline (composition root, contracts, prompts)
- [ ] Dotnet pipeline (composition root, contracts, prompts)
- [ ] Terraform pipeline (composition root, contracts, prompts)

### Phase 6 — Hardening

- [ ] Contract validation retry logic (re-prompt Claude on contract failure)
- [ ] Timeout handling for `claude -p` calls
- [ ] Graceful shutdown and checkpoint save on interrupt (Ctrl+C)
- [ ] Configuration file for retry limits, timeout values, model selection
- [ ] CI integration and automated testing of contracts
