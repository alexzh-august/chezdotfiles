# Team-Shared Functions
# Add common functions here that all team members should have
#
# Usage: Source this file from your ~/.zshrc:
#   source ~/chezdotfiles/dotfiles/shell/zsh/functions.sh

# ==============================================================================
# Directory Operations
# ==============================================================================

# Create directory and cd into it
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# ==============================================================================
# Git Helpers
# ==============================================================================

# Show git branch in prompt-friendly format
git_branch() {
    git branch 2>/dev/null | grep '^*' | colrm 1 2
}

# Quick commit with message
gc() {
    git commit -m "$*"
}

# ==============================================================================
# Development Helpers
# ==============================================================================

# Find process by name
psg() {
    ps aux | grep -v grep | grep -i "$1"
}

# Quick HTTP status check
httpstatus() {
    curl -s -o /dev/null -w "%{http_code}" "$1"
}

# ==============================================================================
# Claude Code Helpers
# ==============================================================================

# Start Claude in a specific directory
claude_in() {
    (cd "$1" && claude)
}
