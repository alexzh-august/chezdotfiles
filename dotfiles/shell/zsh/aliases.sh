# Team-Shared Aliases
# Add common aliases here that all team members should have
#
# Usage: Source this file from your ~/.zshrc:
#   source ~/chezdotfiles/dotfiles/shell/zsh/aliases.sh

# ==============================================================================
# Navigation
# ==============================================================================
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# ==============================================================================
# Git Shortcuts
# ==============================================================================
alias gs='git status'
alias gd='git diff'
alias gds='git diff --staged'
alias gl='git log --oneline -20'
alias gp='git pull'

# ==============================================================================
# Claude Code
# ==============================================================================
alias cc='claude'
alias ccp='claude --print'

# ==============================================================================
# Development
# ==============================================================================
alias serve='python -m http.server 8000'
alias json='python -m json.tool'

# ==============================================================================
# Safety
# ==============================================================================
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
