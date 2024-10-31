import subprocess
import sys
import base64
import time
import json
import requests
from urllib.parse import parse_qs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Define required modules
required_modules = ['base64', 'time', 'json', 'requests', 'urllib.parse', 'Crypto']

# Function to install missing packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check if modules are installed; if not, install them
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Module {module} not found. Installing...")
        if module == 'Crypto':
            install('pycryptodome')  # Install pycryptodome for Crypto
        else:
            install(module)

# Imports after ensuring installation
import base64
import time
import json
import requests
from urllib.parse import parse_qs
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Function to encode event
def encode_event(e, t):
    r = f"{e}|{t}|{int(time.time())}"
    n = "tttttttttttttttttttttttttttttttt"
    i = n[:16]
    key = n.encode('utf-8')
    iv = i.encode('utf-8')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(r.encode('utf-8'), AES.block_size))
    return base64.b64encode(base64.b64encode(encrypted)).decode('utf-8')

# Prompt user for query ID and extract user ID
query_id = input("Enter your query ID: ")
user_id = str(json.loads(parse_qs(query_id)['user'][0])['id'])

# Set headers with the provided query ID
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'access-control-allow-origin': '*',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'lan': 'en',
    'origin': 'https://bbqapp.bbqcoin.ai',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://bbqapp.bbqcoin.ai/',
    'sec-ch-ua': '"Android WebView";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'use-agen': query_id,  # Insert query ID here
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_9; like Mac OS X) AppleWebKit/536.45 (KHTML, like Gecko)  Chrome/47.0.3428.167 Mobile Safari/537.6',
    'x-requested-with': 'org.telegram.messenger',
}

# Set taps to 150000
taps = '150000'
# Set limit for maximum coins
max_coins_limit = 1500000000

# Function to send tap request
def bbq_tap():
    data = {
        'id_user': user_id,
        'mm': taps,
        'game': encode_event(user_id, taps),
    }
    response = requests.post('https://bbqbackcs.bbqcoin.ai/api/coin/earnmoney', headers=headers, data=data)
    response_data = response.json()

    # Check if 'data' exists in response
    if 'data' in response_data:
        total_coins = response_data['data']
        print(f"⚡ Coins Added! Total Coins: {total_coins} 🪙")
        
        # Check if total coins exceed max limit
        if total_coins >= max_coins_limit:
            print(f"Reached or exceeded the limit of {max_coins_limit} coins. Stopping script.")
            return False  # Stop if max coins limit is reached
    else:
        print("⚡ Unexpected response format:", response_data)
    return True  # Continue if limit not reached

# Continuous execution until max_coins_limit is reached
while True:
    if not bbq_tap():
        break
    time.sleep(1)  # Wait for 1 second before the next request
