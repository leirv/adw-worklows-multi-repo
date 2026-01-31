# UI Coder

Implement the frontend code following the `Plan`. Follow the `Instructions` to implement, then `Report` the completed work.

## Instructions

- Read the plan thoroughly before writing any code.
- THINK HARD about the plan, the existing UI patterns, and the best way to implement.
- Focus ONLY on frontend/client code (Vite, React/Vue, components, styles).
- Follow existing patterns in `app/client/**`.
- If a UDR (UI Decision Record) exists for this task, follow its component design exactly.
- If a TDR (Test Design Record) exists, ensure your implementation passes all defined tests.
- Use `npm` or `pnpm` for package management.
- Write clean, reusable components. Follow the project's component patterns.
- Ensure accessibility (ARIA labels, keyboard navigation).
- Do NOT modify backend code - that's for the Backend Coder.
- Run tests and build after implementation to verify zero regressions.

## Relevant Files

Focus on the following files:
- `app/client/**` - Frontend codebase
- `udr/*.md` - UI Decision Records for component design
- `tdr/*.md` - Test Design Records for expected test cases
- `scripts/**` - Client start/stop scripts

Ignore backend files (`app/server/**`).

## Validation Commands

After implementing, run these commands:
- `cd app/client && npm run test` - Run all frontend tests
- `cd app/client && npm run build` - Verify build succeeds
- `cd app/client && npm run lint` - Check for linting errors (if available)

## Plan
$ARGUMENTS

## Report
- Summarize the work you've just done in a concise bullet point list.
- List each file/component created or modified.
- Report the files and total lines changed with `git diff --stat`.
- Confirm all tests pass and build succeeds.
