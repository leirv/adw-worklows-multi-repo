# Task Classifier

Analyze the `Task` and classify it into the appropriate command type. Return ONLY the command - nothing else.

## Instructions

- IMPORTANT: You must return ONLY the command string. No explanations, no reasoning, no extra text.
- Analyze the task description to determine the type of work required.
- Match the task to ONE of the available commands based on the classification rules below.
- If the task is unclear or doesn't fit any category, return `0`.

## Classification Rules

### Planning Commands (create specs/records BEFORE implementation)

| Command | Use When |
|---------|----------|
| `/architect` | System-level decisions, technology choices, component structure, API design |
| `/designer` | Code-level design, class structure, method flows, service interactions |
| `/ui_designer` | UI/UX design, screens, components, user flows, layouts |
| `/test_tdd_designer` | Test design, TDD approach, defining tests before implementation |
| `/feature` | New functionality, adding capabilities, enhancements |
| `/bug` | Fixing errors, crashes, incorrect behavior, regressions |
| `/chore` | Maintenance, refactoring, dependencies, documentation, cleanup |

### Implementation Commands (execute plans)

| Command | Use When |
|---------|----------|
| `/backend_coder` | Implementing server-side code, APIs, services, Python code |
| `/ui_coder` | Implementing frontend code, components, UI, React/Vue/Vite |
| `/tester` | Running tests, validating implementation, final QA |

## Classification Logic

1. **Is it about HIGH-LEVEL ARCHITECTURE?** (system design, tech stack, components)
   → `/architect`

2. **Is it about CODE DESIGN?** (classes, methods, data flow, contracts)
   → `/designer`

3. **Is it about UI/UX?** (screens, components, user flows, visual design)
   → `/ui_designer`

4. **Is it about TESTING STRATEGY?** (what tests to write, TDD, test structure)
   → `/test_tdd_designer`

5. **Is it a NEW FEATURE?** (add, create, implement new functionality)
   → `/feature`

6. **Is it a BUG FIX?** (fix, repair, crash, error, broken, doesn't work)
   → `/bug`

7. **Is it MAINTENANCE?** (refactor, update deps, docs, cleanup, chore)
   → `/chore`

8. **Is it BACKEND IMPLEMENTATION?** (write Python code, implement API, build service)
   → `/backend_coder`

9. **Is it FRONTEND IMPLEMENTATION?** (write UI code, build component, implement screen)
   → `/ui_coder`

10. **Is it VALIDATION/TESTING?** (run tests, verify, validate, QA)
    → `/tester`

## Examples

| Task | Classification |
|------|----------------|
| "Add user authentication with OAuth" | `/feature` |
| "Fix the login button not responding" | `/bug` |
| "Update dependencies to latest versions" | `/chore` |
| "Design the class structure for payment service" | `/designer` |
| "Plan the microservices architecture" | `/architect` |
| "Design the checkout flow screens" | `/ui_designer` |
| "Write tests for the auth module" | `/test_tdd_designer` |
| "Implement the user API endpoint" | `/backend_coder` |
| "Build the login form component" | `/ui_coder` |
| "Validate the payment integration works" | `/tester` |

## Task

$ARGUMENTS

## Response Format

Return ONLY one of these values:
- `/architect`
- `/designer`
- `/ui_designer`
- `/test_tdd_designer`
- `/feature`
- `/bug`
- `/chore`
- `/backend_coder`
- `/ui_coder`
- `/tester`
- `0` (if unclear)

NO other text. Just the command.
