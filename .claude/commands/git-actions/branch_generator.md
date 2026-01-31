# Generate Git Branch Name

Based on the `Instructions` below, take the `Variables` follow the `Run` section to generate a concise Git branch name following the specified format. Then follow the `Report` section to report the results of your work.

## Variables
issue_class: $1
adw_id: $2
issue: $3

## Instructions

- Generate a branch name in the format: `<issue_class>-<concise_name>`
- The `<concise_name>` should be:
  - 3-6 words maximum
  - All lowercase
  - Words separated by hyphens
  - Descriptive of the main task bug or feature
  - No special characters except hyphens
- Examples:
  - `feat-add-user-auth`
  - `bug-fix-login-error`
  - `plan-update-dependencies`
- Extract the issue number, title, and body from the issue JSON