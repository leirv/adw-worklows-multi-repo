# Backend Coder

Implement the backend code following the `Plan`. Follow the `Instructions` to implement, then `Report` the completed work.

## Instructions

- Read the plan thoroughly before writing any code.
- THINK HARD about the plan, the existing codebase patterns, and the best way to implement.
- Focus ONLY on backend/server code (Python, APIs, services, repositories).
- Follow existing patterns in `app/server/**`.
- If a DDR (Design Decision Record) exists for this task, follow its class/method contracts exactly.
- If a TDR (Test Design Record) exists, ensure your implementation passes all defined tests.
- Use `uv` for package management. If you need a new library, use `uv add`.
- Write clean, readable code. Follow the project's coding standards.
- Do NOT modify frontend code - that's for the UI Coder.
- Run tests after implementation to verify zero regressions.

## Relevant Files

Focus on the following files:
- `app/server/**` - Backend codebase
- `ddr/*.md` - Design Decision Records for code contracts
- `tdr/*.md` - Test Design Records for expected test cases
- `scripts/**` - Server start/stop scripts

Ignore frontend files (`app/client/**`).

## Validation Commands

After implementing, run these commands:
- `cd app/server && uv run pytest` - Run all backend tests
- `cd app/server && uv run pytest --cov` - Run tests with coverage (if available)

## Plan
$ARGUMENTS

## Report
- Summarize the work you've just done in a concise bullet point list.
- List each file created or modified.
- Report the files and total lines changed with `git diff --stat`.
- Confirm all tests pass.
