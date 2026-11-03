#!/usr/bin/env bash
# 🏛️ APEX TERMINAL OS — ONE-LINE SOVEREIGN INSTALLER
# Engineered exclusively for Rick Jefferson | RJ Business Solutions
# Configures Homebrew, Zsh, Starship, FZF, Venice Sovereign Neural Router,
# Hermetic Sandbox, Live Canvas Server, Multi-File Forge, and the 12-Ability Startup Menu.

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo -e "\033[1;36m======================================================================\033[0m"
echo -e "\033[1;36m  🏛️  INSTALLING APEX TERMINAL OS (VENICE SOVEREIGN EDITION v2.0)     \033[0m"
echo -e "\033[1;36m======================================================================\033[0m"

# 1. Ensure Homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "==> Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2. Install Foundational CLI Utilities
echo "==> Verifying Core Packages..."
PACKAGES=(
    fzf
    starship
    eza
    bat
    ripgrep
    yt-dlp
    ffmpeg
    cloudflared
    lazygit
    uv
)

for pkg in "${PACKAGES[@]}"; do
    if ! brew list "$pkg" &>/dev/null; then
        echo "--> Installing $pkg..."
        HOMEBREW_NO_AUTO_UPDATE=1 brew install "$pkg" || true
    fi
done

# 3. Setup User Directory & Workspace Architecture
echo "==> Configuring ~/.local/bin, ~/.apex-workspace, and Cheatsheet Repos..."
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.config/arsenal/cheatsheets"
mkdir -p "$HOME/.config"
mkdir -p "$HOME/.apex-workspace"/{sandboxes,canvas,scripts,forge}

# Copy latest cheatsheets and layouts into user config
cp -r "$REPO_DIR/cheatsheets/"* "$HOME/.config/arsenal/cheatsheets/"
cp -r "$REPO_DIR/config/apex-layout.kdl" "$HOME/.config/arsenal/apex-layout.kdl" 2>/dev/null || true
cp -r "$REPO_DIR/config/apex-seatbelt.sb" "$HOME/.config/arsenal/apex-seatbelt.sb" 2>/dev/null || true
cp -r "$REPO_DIR/config/litellm_config.yaml" "$HOME/.config/arsenal/litellm_config.yaml" 2>/dev/null || true

# Install core binaries (apex + venice sovereign OS + RAG + MCP + Keygen + Whitelabel)
cp "$REPO_DIR/bin/apex" "$HOME/.local/bin/apex"
cp "$REPO_DIR/bin/venice" "$HOME/.local/bin/venice"
chmod +x "$HOME/.local/bin/apex" "$HOME/.local/bin/venice"
for extra_bin in apex-agent apex-rag apex-mcp apex-keygen-server apex-whitelabel apex-fulfill; do
    if [ -f "$REPO_DIR/bin/$extra_bin" ]; then
        cp "$REPO_DIR/bin/$extra_bin" "$HOME/.local/bin/$extra_bin"
        chmod +x "$HOME/.local/bin/$extra_bin"
    fi
done
ln -sf "$HOME/.local/bin/apex-whitelabel" "$HOME/.local/bin/apex-monetize" 2>/dev/null || true

# Create all sovereign execution symlinks
SYMLINKS=(
    menu
    m
    apex-menu
    ai
    ask
    apex-sandbox
    sandbox
    do-task
    apex-canvas
    canvas
    apex-forge
    forge
    runlast
    venice-u
    venice-ab
    venice-heretic
    venice-glm
    venice-rp
    venice-gemma
    venice-oss
    venice-cheap
    venice-img
)

for cmd in "${SYMLINKS[@]}"; do
    ln -sf "$HOME/.local/bin/venice" "$HOME/.local/bin/$cmd"
done

# Copy Starship config if not present
if [ ! -f "$HOME/.config/starship.toml" ]; then
    cp "$REPO_DIR/config/starship.toml" "$HOME/.config/starship.toml"
fi

# 4. Inject or Update ~/.zshrc
ZSHRC="$HOME/.zshrc"
touch "$ZSHRC"

if grep -q "# --- APEX TERMINAL OS INITIALIZATION ---" "$ZSHRC"; then
    echo "==> Updating existing Apex Terminal OS block in ~/.zshrc..."
    python3 -c '
import pathlib, re
zshrc = pathlib.Path.home() / ".zshrc"
apex_cfg = (pathlib.Path("'"$REPO_DIR"'") / "config/.zshrc_apex").read_text()
text = zshrc.read_text()
new_block = "# --- APEX TERMINAL OS INITIALIZATION ---\n" + apex_cfg + "\n# --- END APEX TERMINAL OS ---"
text = re.sub(r"# --- APEX TERMINAL OS INITIALIZATION ---.*?# --- END APEX TERMINAL OS ---", new_block, text, flags=re.DOTALL)
zshrc.write_text(text)
'
else
    echo "==> Wiring Apex Terminal OS into ~/.zshrc..."
    echo "" >> "$ZSHRC"
    echo "# --- APEX TERMINAL OS INITIALIZATION ---" >> "$ZSHRC"
    cat "$REPO_DIR/config/.zshrc_apex" >> "$ZSHRC"
    echo "# --- END APEX TERMINAL OS ---" >> "$ZSHRC"
fi

echo -e "\033[1;32m======================================================================\033[0m"
echo -e "\033[1;32m  ✓ APEX TERMINAL OS v2.0 INSTALLED SUCCESSFULLY!                     \033[0m"
echo -e "\033[1;32m======================================================================\033[0m"
echo -e "Run:  \033[1;33msource ~/.zshrc\033[0m"
echo -e "Menu: \033[1;33mm\033[0m or \033[1;33mmenu\033[0m (Launches 13-Ability Command Center)"
echo -e "AI:   \033[1;33mai <natural language>\033[0m | \033[1;33msandbox <task>\033[0m | \033[1;33mcanvas <ui>\033[0m"
echo -e "Sell: \033[1;33mapex-whitelabel\033[0m or \033[1;33mapex-monetize\033[0m (Add your Logo, Brand & Stripe Keys to resell)"
