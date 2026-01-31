# Tester

Perform final validation of the implementation against the `Plan`. Follow the `Instructions` to validate, then `Report` the results.

## Instructions

- IMPORTANT: You are the final quality gate before code is considered complete.
- Read the plan and all related design records (ADR, DDR, UDR, TDR) thoroughly.
- THINK HARD about what "done" means for this task.
- Verify the implementation matches the design specifications.
- Run ALL tests and ensure they pass.
- Check for regressions - existing functionality should not be broken.
- Validate edge cases and error handling.
- If a TDR exists, verify ALL test cases defined in it are implemented and passing.

## Validation Checklist

Verify each item before marking the task as complete:

### Code Quality
- [ ] Code follows project coding standards
- [ ] No obvious bugs or logic errors
- [ ] Error handling is appropriate
- [ ] No hardcoded values that should be configurable

### Test Coverage
- [ ] All test cases from TDR are implemented (if TDR exists)
- [ ] Unit tests pass
- [ ] Integration tests pass (if applicable)
- [ ] Edge cases are tested
- [ ] Error conditions are tested

### Backend Validation (if applicable)
- [ ] `cd app/server && uv run pytest` - All tests pass
- [ ] API endpoints return expected responses
- [ ] Database operations work correctly
- [ ] No breaking changes to existing APIs

### Frontend Validation (if applicable)
- [ ] `cd app/client && npm run test` - All tests pass
- [ ] `cd app/client && npm run build` - Build succeeds
- [ ] UI matches UDR specifications (if UDR exists)
- [ ] Responsive behavior works
- [ ] Accessibility requirements met

### Integration Validation
- [ ] Frontend and backend work together correctly
- [ ] Data flows as expected end-to-end
- [ ] No console errors in browser
- [ ] No server errors in logs

## Relevant Files

- `specs/*.md` - Original task specifications
- `adr/*.md` - Architectural Decision Records
- `ddr/*.md` - Design Decision Records
- `udr/*.md` - UI Decision Records
- `tdr/*.md` - Test Design Records
- `app/server/**` - Backend implementation
- `app/client/**` - Frontend implementation

## Plan
$ARGUMENTS

## Report
- Summarize the validation work you've done in a concise bullet point list.
- Report test results: passed/failed counts.
- List any issues found during validation.
- Report the files and total lines changed with `git diff --stat`.
- Provide final verdict: PASS or FAIL with reasons.

### Report Format

```
## Validation Results

### Tests
- Backend: X passed, Y failed
- Frontend: X passed, Y failed

### Issues Found
- <issue 1 or "None">
- <issue 2>

### Checklist Status
- Code Quality: PASS/FAIL
- Test Coverage: PASS/FAIL
- Backend: PASS/FAIL/N/A
- Frontend: PASS/FAIL/N/A
- Integration: PASS/FAIL/N/A

### Final Verdict: PASS / FAIL
<reason if fail>
```
