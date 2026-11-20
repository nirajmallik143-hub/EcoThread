"""
EcoThread Carbon-Aware Optimizer — Free Tier + Automated 18-Digit Pro Gate
Organization: Mallikgroup-for-Humanity | Architect: Niraj Mallik (©Nirajmallik@hub)
License: MIT License © 2026 Niraj Mallik
"""

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DB_ROOT = "https://nmdc-ajs-security-default-rtdb.firebaseio.com/mallik_payments"
STATE_FILE = Path.home() / ".ecothread_tier.json"
FREE_DAILY_LIMIT = 3


def is_valid_luhn_18(key: str) -> bool:
    if not key or len(key) != 18 or not key.isdigit():
        return False
    total = 0
    for idx, ch in enumerate(reversed(key)):
        d = int(ch)
        if idx % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def check_ecothread_access(key: str = "") -> dict:
    saved = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    candidate = (key or saved.get("pro_key", "")).strip()

    if is_valid_luhn_18(candidate):
        try:
            url = f"{DB_ROOT}/quantum_keys/{candidate}.json"
            with urllib.request.urlopen(url, timeout=10) as resp:
                rec = json.loads(resp.read().decode("utf-8"))
            now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
            if rec and rec.get("status") == "ACTIVE" and int(rec.get("expiresAt", 0)) > now_ms:
                STATE_FILE.write_text(json.dumps({"pro_key": candidate}))
                return {"tier": "PRO", "allowed": True, "key": candidate, "remaining": "UNLIMITED"}
        except Exception:
            pass

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    used = saved.get("count", 0) if saved.get("date") == today else 0
    if used < FREE_DAILY_LIMIT:
        STATE_FILE.write_text(json.dumps({"date": today, "count": used + 1, "pro_key": saved.get("pro_key", "")}))
        return {"tier": "FREE", "allowed": True, "remaining": FREE_DAILY_LIMIT - (used + 1)}

    return {
        "tier": "FREE_LIMIT_REACHED",
        "allowed": False,
        "upgrade_portal": "https://mallikgroup-for-humanity.github.io/mallik-aani-botim-pay/nepal-banks.html",
        "message": "Daily 3-run Free Tier reached. Pay via mBank UAE, Botim/Aani, Card, or Nepal Bank to receive your unique 18-digit Pro key."
    }


if __name__ == "__main__":
    print(json.dumps(check_ecothread_access(), indent=2))
