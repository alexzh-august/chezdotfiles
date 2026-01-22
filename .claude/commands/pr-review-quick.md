# Quick PR Review

Run a quick PR review focusing on critical issues only.

## Usage

```
/pr-review-quick [PR_NUMBER | PR_URL]
```

## Description

This command runs a fast, focused review of a pull request, concentrating on:
- Critical errors and bugs
- Security issues
- Breaking changes
- Major code quality concerns

This is ideal for quick checks before merging or when time is limited.

## Focus Areas

### 1. Critical Errors
- Unhandled exceptions that could crash the application
- Null pointer dereferences
- Resource leaks
- Race conditions

### 2. Security Issues
- SQL injection vulnerabilities
- XSS vulnerabilities
- Sensitive data exposure
- Authentication/authorization bypasses

### 3. Breaking Changes
- API changes that break backward compatibility
- Database schema changes
- Configuration changes

### 4. Major Quality Issues
- Dead code
- Obvious bugs
- Critical performance issues

## Instructions for Claude

When this command is invoked:

1. **Fetch PR information**:
   ```bash
   gh pr view <PR_NUMBER> --json number,title,files
   gh pr diff <PR_NUMBER>
   ```

2. **Run a focused single-pass review**:
   - Focus only on critical and high-priority issues
   - Skip stylistic concerns
   - Skip minor improvements
   - Prioritize speed over comprehensiveness

3. **Generate a concise report**:
   - List only critical and high issues
   - Provide quick fixes where possible
   - Give a clear pass/fail recommendation

## Output Format

```markdown
# Quick PR Review: #<PR_NUMBER>

## Verdict: [PASS / NEEDS ATTENTION / BLOCK]

### Critical Issues (0)
[None found / List critical issues]

### High Priority Issues (0)
[None found / List high priority issues]

### Quick Fixes
[Immediate actionable items]

### Recommendation
[1-2 sentence recommendation on whether to proceed with merge]
```

## When to Use

- Pre-merge sanity check
- Time-constrained reviews
- Simple/small PRs
- Initial triage before full review

## Example

```bash
# Quick review of current branch's PR
/pr-review-quick

# Quick review of specific PR
/pr-review-quick 456
```
