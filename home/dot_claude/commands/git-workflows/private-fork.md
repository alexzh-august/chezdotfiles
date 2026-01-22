# Private Fork

Create a private repository from a public repository while maintaining upstream connection for fetching future changes.

## Arguments

- `$ARGUMENTS` - The URL of the public repository to create a private fork from (e.g., `https://github.com/owner/repo` or `git@github.com:owner/repo.git`)

## Instructions

When the user invokes this command, guide them through creating a private "fork" of a public repository. This is necessary because GitHub does not allow creating private forks of public repositories.

### Step 1: Parse and Validate Input

Extract the repository information from `$ARGUMENTS`:
- Parse the repository URL to extract owner and repo name
- If no arguments provided, ask the user for the source repository URL
- Validate the URL format (support both HTTPS and SSH formats)

### Step 2: Gather Required Information

Ask the user for:
1. **Target repository name** - Name for the new private repository (default: same as source)
2. **GitHub username** - Their GitHub username for the new repo URL
3. **Clone location** - Where to clone the final repository locally (default: current directory)

### Step 3: Execute the Private Fork Workflow

Run the following steps, explaining each one:

```bash
# 1. Create a bare clone of the source repository (temporary)
git clone --bare <source_url>

# 2. Inform user to create new PRIVATE repository on GitHub
# Name: <repo_name>
# Visibility: Private
# Do NOT initialize with README, license, or .gitignore

# 3. Mirror-push the bare clone to the new private repository
cd <repo_name>.git
git push --mirror git@github.com:<username>/<repo_name>.git

# 4. Clean up the temporary bare clone
cd ..
rm -rf <repo_name>.git

# 5. Clone the new private repository
git clone git@github.com:<username>/<repo_name>.git

# 6. Add upstream remote with push disabled
cd <repo_name>
git remote add upstream <source_url>
git remote set-url --push upstream DISABLE

# 7. Verify remotes are configured correctly
git remote -v
```

### Step 4: Verify Setup

Confirm the setup by showing:
- `git remote -v` output showing:
  - `origin` pointing to user's private repo (fetch and push)
  - `upstream` pointing to source repo (fetch only, push DISABLED)

### Step 5: Explain Workflow

After successful setup, explain to the user:

**For pushing changes:**
```bash
git push origin <branch>
```

**For pulling upstream changes:**
```bash
git fetch upstream
git rebase upstream/main  # or upstream/master
# Resolve conflicts if any
git push origin <branch>
```

### Error Handling

- If the bare clone fails, check if the source URL is accessible
- If mirror push fails, verify the user created the private repo and has push access
- If any step fails, provide clear instructions for manual recovery

### Security Notes

- The private repository will contain full history from the public repo
- Sensitive commits from the public repo will be in your private repo's history
- The upstream remote has push disabled to prevent accidental pushes to the original repo
