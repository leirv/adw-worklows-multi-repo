# TDD Test Designer

Create a new TDR (Test Design Record) in `tdr/*.md` to define tests BEFORE implementation using the exact specified markdown `Plan Format`. Follow the `Instructions` to create the test design, use the `Relevant Files` to focus on the right files. Follow the `Report` section to properly report the results of your work.

## Instructions

- IMPORTANT: You're writing a TDR to define tests that will DRIVE the implementation (Test-Driven Development).
- IMPORTANT: The `Task` describes what needs to be built, but we're designing the TESTS FIRST, not the implementation.
- Tests should be written from the perspective of: "What should this code DO? How do we verify it works?"
- Create the TDR in the `tdr/*.md` file. Name it appropriately based on the `Task`.
- Use the plan format below to create the test design.
- Research the codebase to understand existing test patterns and conventions.
- IMPORTANT: Replace every <placeholder> in the `Plan Format` with the requested value.
- Use your reasoning model: THINK HARD about edge cases, error conditions, and what "working correctly" means.
- If a DDR or UDR exists for this task, use it to understand what needs to be tested.
- Respect requested files in the `Relevant Files` section.
- Start your research by reading the `README.md` file.
- When you finish creating the TDR, follow the `Report` section to properly report the results of your work.

## Relevant Files

Focus on the following files:
- `README.md` - Contains the project overview and instructions.
- `app/server/**` - Backend code to understand existing test patterns.
- `app/client/**` - Frontend code to understand existing test patterns.
- `ddr/*.md` - Design Decision Records for understanding code contracts.
- `udr/*.md` - UI Decision Records for understanding component contracts.

## Plan Format

```md
# Task: <Task name>

## Task Description
<describe what needs to be built/tested>

## Test Strategy Overview
<high-level description of the testing approach - what layers, what types of tests>

## Test Categories

### Unit Tests
<tests for individual functions/methods/components in isolation>

### Integration Tests
<tests for multiple components working together>

### End-to-End Tests (if applicable)
<tests for complete user flows>

## Backend Tests

### <TestClassName>
- **File**: `app/server/tests/test_<name>.py`
- **Tests For**: <class/module being tested>

#### Test Cases
| Test Name | Description | Input | Expected Output |
|-----------|-------------|-------|-----------------|
| test_<name>_success | <happy path> | <input data> | <expected result> |
| test_<name>_invalid_input | <validation> | <bad input> | <expected error> |
| test_<name>_edge_case | <edge case> | <edge input> | <expected behavior> |

#### Test Implementation Outline
```python
class <TestClassName>:
    def test_<name>_success(self):
        # Arrange: <setup>
        # Act: <call method>
        # Assert: <verify result>

    def test_<name>_invalid_input(self):
        # Arrange: <setup with bad data>
        # Act & Assert: <verify exception raised>
```

### <Another TestClassName>
<repeat structure as needed>

## Frontend Tests

### <ComponentName>.test.tsx
- **File**: `app/client/src/components/__tests__/<ComponentName>.test.tsx`
- **Tests For**: <component being tested>

#### Test Cases
| Test Name | Description | Setup | Expected Behavior |
|-----------|-------------|-------|-------------------|
| renders_correctly | <initial render> | <props> | <what should appear> |
| handles_user_interaction | <user action> | <setup> | <what should happen> |
| displays_error_state | <error condition> | <error props> | <error UI> |

#### Test Implementation Outline
```typescript
describe('<ComponentName>', () => {
    it('renders correctly', () => {
        // Arrange: render with props
        // Assert: verify elements present
    });

    it('handles user interaction', () => {
        // Arrange: render component
        // Act: simulate user action
        // Assert: verify result
    });
});
```

### <Another ComponentName>
<repeat structure as needed>

## Mocks and Fixtures

### Mocks Needed
| Mock | Purpose | Returns |
|------|---------|---------|
| <service/api> | <why mock it> | <mock response> |

### Test Fixtures
| Fixture | Purpose | Data Shape |
|---------|---------|------------|
| <fixture_name> | <what test data> | <example data> |

## Edge Cases and Error Conditions

| Scenario | Test Coverage | Priority |
|----------|---------------|----------|
| <edge case 1> | <which test covers it> | High/Medium/Low |
| <error condition 1> | <which test covers it> | High/Medium/Low |

## Test Dependencies
<list any test libraries or tools needed>
- pytest (backend)
- pytest-asyncio (if async)
- vitest/jest (frontend)
- @testing-library/react (frontend)

## Definition of Done
- [ ] All test cases defined in this TDR are implemented
- [ ] All tests pass
- [ ] Coverage meets project requirements
- [ ] Edge cases are covered
- [ ] Error conditions are tested

## Notes
<optionally list any additional notes about testing approach>
```

## Task
$ARGUMENTS

## Report
- Summarize the work you've just done in a concise bullet point list.
- Include a path to the TDR you created in the `tdr/*.md` file.
- List the total number of test cases defined.
