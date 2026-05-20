# About this user

NVIDIA engineer (email `nhugi@nvidia.com`, GitHub `NadavHuNV`). Primary machine is a Mac (Apple Silicon, zsh + Oh My Zsh). Frequently works on many Linux VMs as part of his job, sudo on all of them. Sets up new VMs often enough that per-VM friction matters.

Technical depth: comfortable with day-to-day shell use (aliases, git workflow) but not deep on shell internals or dotfile/tooling ecosystems. Frame infrastructure/tooling explanations from first principles; don't assume familiarity with terms like `scp`, raw GitHub URLs, templating systems, or `curl | bash` patterns.

# How to collaborate with this user

**Narrow choices, not menus.** Prefers at most 2 options at a time, recommended one first, with a one-line reason each. Wider option sets (4-5 alternatives) cause disengagement — pre-emptively narrow before presenting.

**Explain before acting.** Before any non-trivial action (file write, command run, anything that changes state), state in plain language what's about to happen and why. He has interrupted tool calls to ask "what is this?" when not pre-briefed — pre-explaining each step prevents that friction.

**Optimize for "one thing to type."** He doesn't want to remember commands for routine workflows. Always prefer single-line / single-action solutions over "do A then B" sequences, even at the cost of mild correctness tradeoffs (e.g. making a repo public to skip auth).

# Shell config / dotfiles

User's shell config is managed by **chezmoi** and hosted publicly at `github.com/NadavHuNV/dotfiles`.

**One-line bootstrap for any new Linux VM:**
```
curl -fsSL https://raw.githubusercontent.com/NadavHuNV/dotfiles/main/install.sh | bash
```
This installs chezmoi, pulls the repo, installs zsh + Oh My Zsh + zsh-autosuggestions + zsh-syntax-highlighting, writes `.zshrc`, and tries to chsh to zsh.

**Repo layout** (at `~/.local/share/chezmoi/` on every machine where this is set up):
- `dot_zshrc.tmpl` — the `.zshrc` template, cross-platform via `{{ if eq .chezmoi.os "darwin" }}` guards (macOS-only: `macos` OMZ plugin, `/opt/homebrew/bin` PATH, `open -e` alias)
- `run_once_before_install-shell.sh.tmpl` — chezmoi hook that installs zsh/OMZ/plugins on Linux only (skipped on macOS)
- `install.sh` — top-level VM bootstrap; ignored by chezmoi via `.chezmoiignore` so it never copies to `$HOME`
- `dot_claude/CLAUDE.md` — this file

**To edit shell config:** edit `~/.local/share/chezmoi/dot_zshrc.tmpl` (NOT `~/.zshrc` directly — direct edits get overwritten on `chezmoi apply`). Then `chezmoi apply` to refresh `~/.zshrc`, then `git -C ~/.local/share/chezmoi commit -am "..." && git -C ~/.local/share/chezmoi push`.

**To update an existing VM:** `chezmoi update` (pulls + re-applies).

**To edit this file (CLAUDE.md):** edit `~/.local/share/chezmoi/dot_claude/CLAUDE.md` on any machine, then commit/push. Other machines pick it up on next `chezmoi update`.
