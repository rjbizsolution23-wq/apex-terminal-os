#!/usr/bin/env python3
"""
🏛️ APEX TERMINAL OS — MULTI-TIER COMMERCIAL PACKAGE BUILDER
Engineered for Rick Jefferson | RJ Business Solutions
Builds the 3 exact commercial distribution archives (.zip and .tar.gz) for:
  1. Tier 1 ($197):   apex-terminal-os-developer-v2.0
  2. Tier 2 ($497):   apex-terminal-os-sovereign-pro-v2.0
  3. Tier 3 ($1,997): apex-terminal-os-enterprise-whitelabel-v2.0
"""

import os
import json
import shutil
import zipfile
import tarfile
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = REPO_ROOT / "dist"
PKG_DIR = REPO_ROOT / "packages"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def make_archives(src_folder: Path, archive_base_name: str):
    zip_path = PKG_DIR / f"{archive_base_name}.zip"
    tar_path = PKG_DIR / f"{archive_base_name}.tar.gz"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file_path in sorted(src_folder.rglob("*")):
            if file_path.is_file():
                arcname = f"{archive_base_name}/{file_path.relative_to(src_folder)}"
                zf.write(file_path, arcname)

    with tarfile.open(tar_path, "w:gz") as tf:
        tf.add(src_folder, arcname=archive_base_name)

    return zip_path, tar_path

def build_all():
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    PKG_DIR.mkdir(parents=True, exist_ok=True)

    # =========================================================================
    # 1. TIER 1: DEVELOPER EDITION ($197)
    # =========================================================================
    dev_dir = DIST_DIR / "developer"
    for sub in ("bin", "cheatsheets", "config", "install"):
        (dev_dir / sub).mkdir(parents=True, exist_ok=True)

    shutil.copy2(REPO_ROOT / "bin/apex", dev_dir / "bin/apex")
    shutil.copy2(REPO_ROOT / "bin/venice", dev_dir / "bin/venice")
    shutil.copy2(REPO_ROOT / "bin/apex-agent", dev_dir / "bin/apex-agent")
    shutil.copy2(REPO_ROOT / "bin/apex-rag", dev_dir / "bin/apex-rag")
    for sheet in sorted((REPO_ROOT / "cheatsheets").glob("0[1-8]-*.txt")):
        shutil.copy2(sheet, dev_dir / "cheatsheets" / sheet.name)
    shutil.copy2(REPO_ROOT / "config/.zshrc_apex", dev_dir / "config/.zshrc_apex")
    shutil.copy2(REPO_ROOT / "config/apex-agent.zsh", dev_dir / "config/apex-agent.zsh")
    shutil.copy2(REPO_ROOT / "config/starship.toml", dev_dir / "config/starship.toml")
    shutil.copy2(REPO_ROOT / "config/apex-seatbelt.sb", dev_dir / "config/apex-seatbelt.sb")
    shutil.copy2(REPO_ROOT / "config/apex-layout.kdl", dev_dir / "config/apex-layout.kdl")
    shutil.copy2(REPO_ROOT / "install/setup.sh", dev_dir / "install/setup.sh")
    shutil.copy2(REPO_ROOT / "README.md", dev_dir / "README.md")
    shutil.copy2(REPO_ROOT / "MASTER_COMMANDS.md", dev_dir / "MASTER_COMMANDS.md")

    (dev_dir / "LICENSE-DEVELOPER.md").write_text("""# 🏛️ APEX TERMINAL OS v2.0 — DEVELOPER EDITION LICENSE ($197)
**Issued by:** RJ Business Solutions (Rick Jefferson, CEO)  
**Permitted Activations:** 1 Personal macOS Workstation  
**Included Modules:**
- 17-Ability Startup Command Center (`m` / `menu`)
- `apex-agent` Claude-Code-Style Agentic Coding Loop (`ax`, `axp`, `axy`)
- 500+ Command Fuzzy Arsenal (`apex` + Cheatsheets 01–08)
- Hermetic Sandbox Runner (`sandbox`) & `runlast`
- Live Interactive HTML5/Tailwind Canvas Server (`canvas` on port 7799)
- 1-Click Automated macOS Installer (`./install/setup.sh`)

© 2026 RJ Business Solutions · 1342 NM 333, Tijeras, New Mexico 87059
""", encoding="utf-8")

    # =========================================================================
    # 2. TIER 2: SOVEREIGN FULL-SPECTRUM SUITE — PRO EDITION ($497)
    # =========================================================================
    sov_dir = DIST_DIR / "sovereign-pro"
    shutil.copytree(dev_dir, sov_dir)
    (sov_dir / "LICENSE-DEVELOPER.md").unlink()
    shutil.copy2(REPO_ROOT / "bin/apex-mcp", sov_dir / "bin/apex-mcp")
    shutil.copy2(REPO_ROOT / "config/litellm_config.yaml", sov_dir / "config/litellm_config.yaml")
    shutil.copy2(REPO_ROOT / "cheatsheets/09-venice-uncensored.txt", sov_dir / "cheatsheets/09-venice-uncensored.txt")
    shutil.copy2(REPO_ROOT / "cheatsheets/10-open-source-ai-agents.txt", sov_dir / "cheatsheets/10-open-source-ai-agents.txt")

    (sov_dir / "LICENSE-SOVEREIGN-PRO.md").write_text("""# 🏛️ APEX TERMINAL OS v2.0 — SOVEREIGN FULL-SPECTRUM PRO LICENSE ($497)
**Issued by:** RJ Business Solutions (Rick Jefferson, CEO)  
**Permitted Activations:** Up to 5 macOS Workstations (Founder / Agency Pro)  
**Included Modules:**
- Everything in Developer Edition (`apex-agent`, 17-Ability Command Center, Sandbox, Canvas)
- Complete 2-Stage Semantic Neural Auto-Router across all 9 Venice Uncensored, Obliterated (`abliteration-abliterated-model-large-v2`), Frontier (`zai-org-glm-5-2`), Heretic, Roleplay, Gemma 4, OSS 120B, E2EE & Lustify v8 Image Studio models
- Cheatsheet `09-venice-uncensored.txt` & `10-open-source-ai-agents.txt`
- Model Context Protocol (MCP) Server (`apex-mcp`)
- Universal LiteLLM Multi-Provider Gateway & RAG Corpus (`apex-rag`)
- Multi-File Full-Stack Project Forge (`forge`)
- Zero-Downtime Sovereign Failover Engine (Venice + GLM + OpenRouter + Ollama $0 automatic backup routing)
- Adversarial Git Security Auditor (`uaudit` & `aicommit`)

© 2026 RJ Business Solutions · 1342 NM 333, Tijeras, New Mexico 87059
""", encoding="utf-8")

    # =========================================================================
    # 3. TIER 3: ENTERPRISE AGENCY FLEET & WHITE-LABEL EDITION ($1,997)
    # =========================================================================
    ent_dir = DIST_DIR / "enterprise-whitelabel"
    shutil.copytree(sov_dir, ent_dir)
    (ent_dir / "LICENSE-SOVEREIGN-PRO.md").unlink()
    shutil.copy2(REPO_ROOT / "bin/apex-whitelabel", ent_dir / "bin/apex-whitelabel")
    shutil.copy2(REPO_ROOT / "bin/apex-fulfill", ent_dir / "bin/apex-fulfill")
    shutil.copy2(REPO_ROOT / "bin/apex-keygen-server", ent_dir / "bin/apex-keygen-server")
    (ent_dir / "enterprise").mkdir(parents=True, exist_ok=True)
    (ent_dir / "landing").mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "landing/index.html", ent_dir / "landing/index.html")

    (ent_dir / "cheatsheets/11-enterprise-sop.txt").write_text("""# 🏛️ ENTERPRISE FLEET & WHITE-LABEL OPERATIONS

# --- White-Label Custom Branding ---
apex-whitelabel --brand "YOUR AGENCY NAME" --tagline "Autonomous Engineering OS" : Custom brand the 12-Ability Startup Command Center
apex-whitelabel --status : Inspect current active white-label branding configuration
apex-whitelabel --reset : Revert to default RJ Business Solutions branding

# --- Commercial License Provisioning ---
apex-fulfill dev client@domain.com : Generate checksum-verified $197 Developer License key
apex-fulfill pro client@domain.com : Generate checksum-verified $497 Sovereign Pro License key
apex-fulfill ent client@domain.com : Generate checksum-verified $1,997 Enterprise License key
""", encoding="utf-8")

    fleet_sh = ent_dir / "enterprise/fleet-deploy.sh"
    fleet_sh.write_text("""#!/usr/bin/env bash
# 🏛️ APEX TERMINAL OS — ENTERPRISE MULTI-MAC SSH FLEET PROVISIONER
# Deploys Apex Terminal OS + Custom Agency White-Label Branding across engineering workstations.
set -e
BRAND="${1:-ENTERPRISE ENGINEERING OS}"
TAGLINE="${2:-AUTONOMOUS COMMAND CENTER}"
echo "==> Deploying Enterprise Fleet Branding: $BRAND ($TAGLINE)"
"$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/install/setup.sh"
"$HOME/.local/bin/apex-whitelabel" --brand "$BRAND" --tagline "$TAGLINE"
echo "✓ Enterprise workstation provisioned."
""", encoding="utf-8")
    fleet_sh.chmod(0o755)

    (ent_dir / "LICENSE-ENTERPRISE-WHITELABEL.md").write_text("""# 🏛️ APEX TERMINAL OS v2.0 — ENTERPRISE FLEET & WHITE-LABEL LICENSE ($1,997)
**Issued by:** RJ Business Solutions (Rick Jefferson, CEO)  
**Permitted Activations:** Unlimited Internal Workstations + Commercial White-Label Client Deployment Rights  
**Included Modules:**
- Everything in Sovereign Full-Spectrum Pro Edition
- **White-Label Rebranding CLI (`apex-whitelabel`)**: Rebrand the Startup Command Center and terminal headers with your agency's name
- **Client License Fulfillment Generator (`apex-fulfill`)**: Generate deterministic license keys for your own clients
- **Enterprise Multi-Mac Fleet Deployer (`enterprise/fleet-deploy.sh`)**
- **White-Label Sales Landing Page Template (`landing/index.html`)**
- **1-on-1 Enterprise Architecture Consultation with Rick Jefferson**

© 2026 RJ Business Solutions · 1342 NM 333, Tijeras, New Mexico 87059
""", encoding="utf-8")

    # Package all 3 tiers into .zip and .tar.gz
    manifest = {"version": "2.0.0", "packages": {}}
    tiers_meta = [
        ("developer", dev_dir, "apex-terminal-os-developer-v2.0", "$197", "RJ-DEV-2026"),
        ("sovereign", sov_dir, "apex-terminal-os-sovereign-pro-v2.0", "$497", "RJ-SOV-2026"),
        ("enterprise", ent_dir, "apex-terminal-os-enterprise-whitelabel-v2.0", "$1,997", "RJ-ENT-2026"),
    ]

    for key, folder, base_name, price, master_code in tiers_meta:
        zip_p, tar_p = make_archives(folder, base_name)
        manifest["packages"][key] = {
            "tier": key,
            "price": price,
            "master_unlock_code": master_code,
            "zip_file": f"packages/{zip_p.name}",
            "zip_size_bytes": zip_p.stat().st_size,
            "zip_sha256": sha256_file(zip_p),
            "tar_file": f"packages/{tar_p.name}",
            "tar_size_bytes": tar_p.stat().st_size,
            "tar_sha256": sha256_file(tar_p),
        }
        print(f"✓ Built {key.upper()} ({price}): {zip_p.name} ({zip_p.stat().st_size} bytes) | SHA256: {manifest['packages'][key]['zip_sha256'][:16]}...")

    (PKG_DIR / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    shutil.rmtree(DIST_DIR)
    print(f"✓ Wrote cryptographic package manifest: {PKG_DIR / 'MANIFEST.json'}")

if __name__ == "__main__":
    build_all()
