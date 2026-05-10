import requests
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

API_KEY = os.getenv("OPENROUTER_API_KEY")
r = requests.get("https://openrouter.ai/api/v1/models", headers={"Authorization": f"Bearer {API_KEY}"})

free = [m['id'] for m in r.json()['data'] if m.get('pricing', {}).get('prompt') == '0']
print(f"Bezmaksas modeļi ({len(free)}):")
for m in free[:15]:
    print(f"  {m}")