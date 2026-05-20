#!/usr/bin/env bash
# One-shot bootstrap for new Linux VMs. Installs chezmoi, pulls dotfiles,
# installs zsh + Oh My Zsh + plugins, and sets zsh as the default shell.
#
# Usage on a new VM:
#   curl -fsSL https://raw.githubusercontent.com/NadavHuNV/dotfiles/main/install.sh | bash

set -euo pipefail

BINDIR="$HOME/.local/bin"
mkdir -p "$BINDIR"

if ! command -v chezmoi >/dev/null 2>&1; then
    echo "==> Installing chezmoi to $BINDIR"
    sh -c "$(curl -fsLS get.chezmoi.io)" -- -b "$BINDIR"
fi

export PATH="$BINDIR:$PATH"

echo "==> Applying dotfiles from NadavHuNV/dotfiles"
chezmoi init --apply NadavHuNV/dotfiles

cat <<'EOF'

Setup complete.

Start a new shell or run:  exec zsh -l
EOF
