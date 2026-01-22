# Lazy Loading for Heavy Tools
# Defer loading of slow tools until first use
#
# Usage: Source this file from your ~/.zshrc:
#   source ~/chezdotfiles/dotfiles/shell/zsh/lazy.sh
#
# This improves shell startup time by only loading tools when needed.

# ==============================================================================
# NVM (Node Version Manager)
# ==============================================================================
# Uncomment if you use nvm - it's notoriously slow to load
#
# lazy_load_nvm() {
#     unset -f nvm node npm npx
#     export NVM_DIR="$HOME/.nvm"
#     [ -s "$NVM_DIR/nvm.sh" ] && source "$NVM_DIR/nvm.sh"
# }
# nvm() { lazy_load_nvm; nvm "$@"; }
# node() { lazy_load_nvm; node "$@"; }
# npm() { lazy_load_nvm; npm "$@"; }
# npx() { lazy_load_nvm; npx "$@"; }

# ==============================================================================
# Pyenv
# ==============================================================================
# Uncomment if you use pyenv
#
# lazy_load_pyenv() {
#     unset -f pyenv
#     export PYENV_ROOT="$HOME/.pyenv"
#     export PATH="$PYENV_ROOT/bin:$PATH"
#     eval "$(pyenv init -)"
# }
# pyenv() { lazy_load_pyenv; pyenv "$@"; }

# ==============================================================================
# Conda
# ==============================================================================
# Uncomment if you use conda
#
# lazy_load_conda() {
#     unset -f conda
#     __conda_setup="$("$HOME/miniconda3/bin/conda" 'shell.zsh' 'hook' 2>/dev/null)"
#     if [ $? -eq 0 ]; then
#         eval "$__conda_setup"
#     fi
# }
# conda() { lazy_load_conda; conda "$@"; }

# ==============================================================================
# Ruby (rbenv)
# ==============================================================================
# Uncomment if you use rbenv
#
# lazy_load_rbenv() {
#     unset -f rbenv ruby gem
#     eval "$(rbenv init -)"
# }
# rbenv() { lazy_load_rbenv; rbenv "$@"; }
# ruby() { lazy_load_rbenv; ruby "$@"; }
# gem() { lazy_load_rbenv; gem "$@"; }
