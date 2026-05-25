import requests
import json

TOKEN = "5657df5933394aa1ae8625b06953f548"
HEADERS = {"X-Auth-Token": TOKEN}

r = requests.get(
    "https://api.football-data.org/v4/competitions/BSA/standings",
    headers=HEADERS
)
print(r.status_code)
print(json.dumps(r.json(), indent=2)[:1000])