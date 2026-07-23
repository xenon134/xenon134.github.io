import sys
import json
import os
import argparse
from supabase import create_client, Client

parser = argparse.ArgumentParser(description="Download transactions from Supabase")
parser.add_argument('--username', help='Username for authentication')
parser.add_argument('--password', help='Password for authentication')
parser.add_argument('output_path', nargs='?', default='transactions.json', help='Output file path (default: transactions.json)')
args = parser.parse_args()

url = 'https://wytmkdjzsagjccqbzflr.supabase.co'
key = 'sb_publishable_h9zWKx6vVMBS0bNTt_3Xag_Y4eMVsfk'

if args.username:
    username = args.username
else:
    username = input('Username: ')

email = f"{username.strip().lower()}@dummy.com"

if args.password:
    password = args.password
else:
    password = input('Password: ')

supabase = create_client(url, key)

if email and password:
    try:
        supabase.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as e:
        print(f"Auth error: {e}")
        sys.exit(1)

# Fetch data matching the requested fields
response = supabase.table("transactions").select("name, desc, amts, time").execute()

data = {
    "transactions": sorted(response.data, key=lambda tx: tx['time'])
}

# Determine output path, defaulting to local directory
output_path = args.output_path
if os.path.isdir(output_path):
    output_path = os.path.join(output_path, "transactions.json")

# Write JSON data to the file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(f"Downloaded {len(response.data)} transactions to {output_path}")
