import urllib.request
import json

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

token = config['token']
print(f"Token length: {len(token)}")

req = urllib.request.Request(
    'https://discord.com/api/v9/users/@me',
    headers={
        'Authorization': token,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        data = json.loads(response.read().decode('utf-8'))
        print(f"Username: {data.get('username')}")
except urllib.error.HTTPError as e:
    print(f"Error: {e.code} {e.reason}")
