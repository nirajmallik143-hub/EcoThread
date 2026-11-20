"""
EcoThread Customer Payment -> Unique 18-Digit Pro Key Bridge
Organization: Mallikgroup-for-Humanity | Architect: Niraj Mallik (©Nirajmallik@hub)
License: MIT License © 2026 Niraj Mallik
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path.home() / "mallik-aani-botim-pay"))
from auto_payment_key_engine import issue_key_for_paid_customer, load_env


def unlock_paid_ecothread_user(
    customer_name: str,
    customer_whatsapp: str,
    order_ref: str,
    payment_rail: str = "mBank UAE / Botim",
    amount_paid: str = "19 AED",
    duration_days: int = 30
) -> dict:
    env = load_env()
    fb_token = env.get("FIREBASE_AUTH_TOKEN", "")
    return issue_key_for_paid_customer(
        customer_name=customer_name,
        customer_whatsapp=customer_whatsapp,
        order_ref=order_ref,
        payment_rail=payment_rail,
        amount_paid=amount_paid,
        product="EcoThread Carbon-Aware Pro",
        duration_days=duration_days,
        firebase_token=fb_token
    )


if __name__ == "__main__":
    print(json.dumps({"bridge": "EcoThread -> Auto 18-Digit Key Engine", "status": "READY"}, indent=2))
