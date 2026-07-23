from __future__ import annotations

from datetime import datetime
from typing import Any

from supabase import create_client


SUPABASE_URL = "https://wytmkdjzsagjccqbzflr.supabase.co"
SUPABASE_KEY = "sb_publishable_h9zWKx6vVMBS0bNTt_3Xag_Y4eMVsfk"

# Replace these with the username/password you want to use for the upload.
USERNAME = "deep"
PASSWORD = "deep"


# Replace this list with the transactions you want to insert.
# Requested shape:
# {
#   "name": "Mr Abhra/IDIB/abhramaitra32",
#   "amt": 35,
#   "date": "14-May-2026",
# }
TRANSACTIONS: list[dict[str, Any]] = [
  {"name": "Mr Abhra/IDIB/abhramaitra32", "amt": 35, "date": "14-May-2026"},
  {"name": "NESCAFE/YESB/paytm.s1prxgj", "amt": -110, "date": "14-May-2026"},
  {"name": "BISHAL K/YESB/q548466032", "amt": -10, "date": "14-May-2026"},
  {"name": "MAHESWAR/BKID/maheswardas9903", "amt": -20, "date": "14-May-2026"},
  {"name": "AAMAR KO/HDFC", "amt": -19, "date": "14-May-2026"},
  {"name": "BISHAL/YESB/q702732888", "amt": -10, "date": "14-May-2026"},
  {"name": "SHREE RA/BARB/ranis81008218", "amt": -100, "date": "14-May-2026"},
  {"name": "AAMAR KO/HDFC", "amt": -19, "date": "15-May-2026"},
  {"name": "PURNIMA/UTIB/9732258243", "amt": -50, "date": "15-May-2026"},
  {"name": "BBNOW/HDFC", "amt": -178.17, "date": "16-May-2026"},
  {"name": "Euronet/UTIB/gpayrecharge2", "amt": -69, "date": "19-May-2026"},
  {"name": "Dough As/YESB/paytm.s10hkd3", "amt": -85, "date": "19-May-2026"},
  {"name": "RAMESH/YESB/q974247727", "amt": -38, "date": "19-May-2026"},
  {"name": "BANDANA/YESB/q633800870", "amt": -55, "date": "19-May-2026"},
  {"name": "UTIITSL/HDFC", "amt": -71.9, "date": "20-May-2026"},
  {"name": "BANDANA/YESB/q633800870", "amt": -20, "date": "20-May-2026"},
  {"name": "UTIITSL/HDFC", "amt": 71.9, "date": "20-May-2026"},
  {"name": "SAMIRAN/SBIN/samiran.roy", "amt": -5, "date": "21-May-2026"},
  {"name": "P2V/samiran.roy", "amt": 5, "date": "21-May-2026"},
  {"name": "DEBORUPA/PUNB/mukherjeedeboru", "amt": -5, "date": "21-May-2026"},
  {"name": "MANORANJ/INDB/bajajpay.687972", "amt": -35, "date": "21-May-2026"},
  {"name": "CREAMY C/YESB/q377893327", "amt": -10, "date": "22-May-2026"},
  {"name": "MANUEL G/UCBA/6290665031", "amt": -325, "date": "22-May-2026"},
  {"name": "SUDIPTA/PUNB/sudipta.band", "amt": 400, "date": "22-May-2026"},
  {"name": "Argha Gh/YESB/paytm.s27tcfd", "amt": -10, "date": "22-May-2026"},
  {"name": "JOY SANT/YESB/q429750725", "amt": -95, "date": "22-May-2026"},
  {"name": "MANORANJ/INDB/bajajpay.687972", "amt": -75, "date": "23-May-2026"},
  {"name": "Indian R/SBIN/railsbiupi11.80", "amt": -10, "date": "24-May-2026"},
  {"name": "SHAMA KH/YESB/q411289557", "amt": -190, "date": "24-May-2026"},
  {"name": "AKHTAR H/YESB/paytm.s27dr91", "amt": -20, "date": "24-May-2026"},
  {"name": "AAMAR KO/HDFC", "amt": -14.25, "date": "24-May-2026"},
  {"name": "AAMAR KO/HDFC", "amt": -100, "date": "24-May-2026"},
  {"name": "MANORANJ/INDB/bajajpay.687972", "amt": -10, "date": "24-May-2026"},
  {"name": "Priyanka/YESB/paytm.s24kufk", "amt": -10, "date": "26-May-2026"},
  {"name": "RAMESH/YESB/q974247727", "amt": -45, "date": "26-May-2026"},
  {"name": "SWIGGY/ICIC/upiswiggy", "amt": -385, "date": "28-May-2026"},
  {"name": "UTTHAN S/YESB/q988508963", "amt": -20, "date": "29-May-2026"},
  {"name": "Ms Runa/YESB/q230428671", "amt": -684, "date": "31-May-2026"},
  {"name": "AAMAR KO/HDFC", "amt": -19, "date": "31-May-2026"}
]


def validate_transaction(transaction: dict[str, Any]) -> None:
    required_keys = {"name", "amt", "date"}
    missing = required_keys - transaction.keys()
    if missing:
        raise ValueError(f"Transaction is missing keys: {sorted(missing)}")

    if not isinstance(transaction["name"], str) or not transaction["name"].strip():
        raise ValueError("Transaction name must be a non-empty string")

    if not isinstance(transaction["amt"], (int, float)):
        raise ValueError("Transaction amt must be numeric")

    if not isinstance(transaction["date"], str) or not transaction["date"].strip():
        raise ValueError("Transaction date must be a non-empty string")

    datetime.strptime(transaction["date"], "%d-%b-%Y")


def to_supabase_row(transaction: dict[str, Any]) -> dict[str, Any]:
    parsed_date = datetime.strptime(transaction["date"], "%d-%b-%Y")
    time_value = parsed_date.strftime("%Y-%m-%dT00:00:00+05:30")
    return {
        "name": transaction["name"].strip(),
        "desc": "",
        "time": time_value,
        "balanced": False,
        "amts": [
            {
                "wallet": "UPI",
                "amt": transaction["amt"],
            }
        ],
    }


def main() -> None:
    if USERNAME == "your_username_here" or PASSWORD == "your_password_here":
        raise ValueError("Set USERNAME and PASSWORD in upload_trans.py before running it")

    rows = []
    for transaction in TRANSACTIONS:
        validate_transaction(transaction)
        rows.append(to_supabase_row(transaction))

    email = f"{USERNAME.strip().lower()}@dummy.com"
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    auth_result = supabase.auth.sign_in_with_password({"email": email, "password": PASSWORD})
    if getattr(auth_result, "user", None) is None:
        raise RuntimeError("Authentication succeeded but no user session was returned")

    response = supabase.table("transactions").insert(rows).execute()

    inserted_rows = getattr(response, "data", []) or []
    print(f"Logged in as {email}")
    print(f"Inserted {len(inserted_rows)} transaction(s)")
    for row in inserted_rows:
        print(f"- {row.get('id')}: {row.get('name')}")


if __name__ == "__main__":
    main()