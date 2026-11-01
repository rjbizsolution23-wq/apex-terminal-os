#!/usr/bin/env python3
"""
APEX TERMINAL OS v2.0 — Live Stripe Product, Price & Payment Link Provisioner
Engineered for Rick Jefferson | RJ Business Solutions
Reads STRIPE_RESTRICTED_KEY from ~/.apex-workspace/.env (never hardcoded in git).
"""
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ENV_PATH = Path.home() / ".apex-workspace" / ".env"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "packages" / "STRIPE_LINKS.json"


def load_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def stripe_post(endpoint: str, data: dict[str, str], api_key: str) -> dict:
    url = f"https://api.stripe.com/v1/{endpoint}"
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=encoded,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Stripe API error on {endpoint} ({e.code}): {err_body}") from e


def main() -> None:
    env = load_env(ENV_PATH)
    rk = env.get("STRIPE_RESTRICTED_KEY") or os.environ.get("STRIPE_RESTRICTED_KEY")
    pk = env.get("STRIPE_PUBLISHABLE_KEY") or os.environ.get("STRIPE_PUBLISHABLE_KEY")
    if not rk:
        raise SystemExit("ERROR: STRIPE_RESTRICTED_KEY not found in environment or ~/.apex-workspace/.env")

    base_delivery_url = "https://rjbizsolution23-wq.github.io/apex-terminal-os/"

    tiers = [
        {
            "id": "developer",
            "name": "Apex Terminal OS v2.0 — Developer Edition",
            "description": (
                "9-Model Semantic Uncensored Router, 12-Ability Startup Menu, "
                "9 FZF Cheatsheets (450+ recipes), and Modern Zsh/Rust CLI Stack."
            ),
            "amount_cents": 19700,
            "price_display": "$197.00 USD",
            "zip_file": "packages/apex-terminal-os-developer-v2.0.zip",
            "tar_file": "packages/apex-terminal-os-developer-v2.0.tar.gz",
            "unlock_code": "RJ-DEV-2026",
        },
        {
            "id": "sovereign",
            "name": "Apex Terminal OS v2.0 — Sovereign Full-Spectrum Suite",
            "description": (
                "Complete Developer Edition + Hermetic Self-Healing Docker/Python Sandbox "
                "(Ability 8), Live Visual Canvas Server (Ability 9), Multi-File Project Forge "
                "(Ability 10), and Zero-Downtime Sovereign Failover."
            ),
            "amount_cents": 49700,
            "price_display": "$497.00 USD",
            "zip_file": "packages/apex-terminal-os-sovereign-pro-v2.0.zip",
            "tar_file": "packages/apex-terminal-os-sovereign-pro-v2.0.tar.gz",
            "unlock_code": "RJ-SOV-2026",
        },
        {
            "id": "enterprise",
            "name": "Apex Terminal OS v2.0 — Enterprise Agency Fleet & White-Label",
            "description": (
                "Complete Sovereign Suite + Commercial White-Label Rebranding CLI "
                "(bin/apex-whitelabel), License Fulfillment Generator (bin/apex-fulfill), "
                "Executive Sales Landing Page Source, and Unlimited Agency Seat License."
            ),
            "amount_cents": 199700,
            "price_display": "$1,997.00 USD",
            "zip_file": "packages/apex-terminal-os-enterprise-whitelabel-v2.0.zip",
            "tar_file": "packages/apex-terminal-os-enterprise-whitelabel-v2.0.tar.gz",
            "unlock_code": "RJ-ENT-2026",
        },
    ]

    results: dict[str, dict] = {}

    for t in tiers:
        print(f"==> Provisioning Stripe Product: {t['name']} ({t['price_display']})...")
        prod = stripe_post(
            "products",
            {
                "name": t["name"],
                "description": t["description"],
                "statement_descriptor": "RJ BIZ APEX OS",
                "metadata[tier]": t["id"],
                "metadata[version]": "2.0.0",
                "metadata[zip_file]": t["zip_file"],
                "metadata[unlock_code]": t["unlock_code"],
            },
            rk,
        )

        price = stripe_post(
            "prices",
            {
                "product": prod["id"],
                "unit_amount": str(t["amount_cents"]),
                "currency": "usd",
                "metadata[tier]": t["id"],
            },
            rk,
        )

        redirect_url = (
            f"{base_delivery_url}?paid_tier={t['id']}"
            f"&unlock={t['unlock_code']}"
            f"&session_id={{CHECKOUT_SESSION_ID}}"
        )

        plink = stripe_post(
            "payment_links",
            {
                "line_items[0][price]": price["id"],
                "line_items[0][quantity]": "1",
                "after_completion[type]": "redirect",
                "after_completion[redirect][url]": redirect_url,
                "allow_promotion_codes": "true",
                "billing_address_collection": "auto",
                "metadata[tier]": t["id"],
                "metadata[unlock_code]": t["unlock_code"],
                "metadata[zip_file]": t["zip_file"],
            },
            rk,
        )

        results[t["id"]] = {
            "tier": t["id"],
            "name": t["name"],
            "price_display": t["price_display"],
            "amount_cents": t["amount_cents"],
            "product_id": prod["id"],
            "price_id": price["id"],
            "payment_link_id": plink["id"],
            "payment_link_url": plink["url"],
            "redirect_delivery_url": redirect_url,
            "zip_file": t["zip_file"],
            "tar_file": t["tar_file"],
            "unlock_code": t["unlock_code"],
        }
        print(f"    [+] Product ID:      {prod['id']}")
        print(f"    [+] Price ID:        {price['id']}")
        print(f"    [+] Payment Link:    {plink['url']}")
        print(f"    [+] Auto-Delivery:   {redirect_url}\n")

    payload = {
        "product": "Apex Terminal OS v2.0",
        "vendor": "RJ Business Solutions",
        "publishable_key": pk or "",
        "generated_at": "2026-11-01",
        "tiers": results,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved Stripe metadata to {OUT_PATH}")


if __name__ == "__main__":
    main()
