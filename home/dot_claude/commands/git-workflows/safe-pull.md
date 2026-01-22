# Safe Pull (Dry Run)

Preview what would happen when pulling changes from upstream without actually modifying your local repository.

## Arguments

- `$ARGUMENTS` - Optional: remote name and branch (e.g., `upstream main`, `origin develop`). Defaults to `upstream` remote and current branch.

## Instructions

When the user invokes this command, perform a safe dry-run analysis of what would happen if they pulled from the specified upstream remote.

### Step 1: Parse Arguments and Validate

Parse `$ARGUMENTS` to determine:
- **Remote name** (default: `upstream`, common alternatives: `origin`)
- **Branch name** (default: current branch or `main`/`master`)

Validate the remote exists:
```bash
git remote -v
```

If the specified remote doesn't exist, show available remotes and ask which one to use.

### Step 2: Fetch Without Merging

Fetch the latest changes from the remote without modifying the working tree:

```bash
git fetch <remote> <branch>
```

This updates remote-tracking branches but doesn't change your local files.

### Step 3: Analyze the Difference

Show what would change if the user pulled:

#### 3a. Commit Summary
```bash
# Show commits that would be pulled (commits on remote not in local)
git log --oneline HEAD..<remote>/<branch>
```

#### 3b. Detailed Changes
```bash
# Show file-level diff statistics
git diff --stat HEAD..<remote>/<branch>

# Show number of files changed, insertions, deletions
git diff --shortstat HEAD..<remote>/<branch>
```

#### 3c. File List
```bash
# List files that would be modified
git diff --name-only HEAD..<remote>/<branch>

# With change type (Added, Modified, Deleted)
git diff --name-status HEAD..<remote>/<branch>
```

### Step 4: Conflict Prediction

Check for potential merge conflicts:

```bash
# Perform a dry-run merge to detect conflicts
git merge --no-commit --no-ff <remote>/<branch>
# Then immediately abort
git merge --abort
```

Report:
- Files that would merge cleanly
- Files with potential conflicts
- Type of conflict (content, rename, delete)

### Step 5: Present Summary Report

Format the output as a clear report:

```
=== Safe Pull Preview ===

Remote: <remote>/<branch>
Local:  <current_branch>

--- Incoming Changes ---
Commits: X new commits would be pulled
Files:   Y files would be changed
  - Z additions
  - W modifications
  - V deletions

--- Commit Log ---
<abbreviated commit log>

--- Changed Files ---
<file list with change types>

--- Conflict Analysis ---
<conflict prediction results>

=== Recommended Action ===
<suggestion based on analysis>
```

### Step 6: Offer Options

After showing the preview, offer the user these options:

1. **Pull with rebase** (recommended for clean history):
   ```bash
   git pull --rebase <remote> <branch>
   ```

2. **Pull with merge** (preserves merge history):
   ```bash
   git pull <remote> <branch>
   ```

3. **Fetch only** (already done, just update tracking branches):
   ```bash
   # Already fetched, no action needed
   ```

4. **Abort** (do nothing, keep current state)

### Advanced Options

If the user wants more details:

**View specific file diff:**
```bash
git diff HEAD..<remote>/<branch> -- <filename>
```

**View commit details:**
```bash
git show <commit_hash>
```

**Check divergence:**
```bash
# Commits only on local (would need to be pushed)
git log --oneline <remote>/<branch>..HEAD

# Commits only on remote (would be pulled)
git log --oneline HEAD..<remote>/<branch>

# Show full divergence
git log --oneline --left-right HEAD...<remote>/<branch>
```

### Common Scenarios

**Scenario 1: No changes to pull**
```
Remote is up to date with local. Nothing to pull.
```

**Scenario 2: Clean fast-forward possible**
```
X commits can be cleanly fast-forwarded. No conflicts expected.
Recommended: git pull --rebase <remote> <branch>
```

**Scenario 3: Merge required**
```
Local and remote have diverged. Merge or rebase required.
Local commits: Y
Remote commits: X
Recommended: Review changes carefully before pulling.
```

**Scenario 4: Conflicts detected**
```
WARNING: Potential conflicts detected in Z files.
Conflicting files:
- path/to/file1.js
- path/to/file2.py

Recommended: Backup your work before pulling.
```

### Error Handling

- If remote doesn't exist: List available remotes
- If branch doesn't exist: List available branches on remote
- If not in a git repository: Inform user and exit
- If network error: Suggest checking connection and retry
