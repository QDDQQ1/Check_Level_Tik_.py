import os
import re
import json
import asyncio
import aiohttp
import telebot
import SignerPy
import time
from datetime import datetime

# إعداد الألوان
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# الإدخالات
from cfonts import render
import time, os, requests, json, webbrowser
C = '\033[1;34m'; E = '\033[1;33m'; R = "\033[1;31m"; G = '\033[1;97m'; W = '\x1b[0m'
a3 = '\x1b[1;32m'; a4 = '\x1b[1;33m'; P2 = '\x1b[38;5;190m'
J21 = '\x1b[38;5;204m'; J22 = '\x1b[38;5;209m'; RED = '\x1b[1;31m'

def banner():
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"""{C}┃{E}   {R}TikTok Tool{C}     ┃ {R}Dev: {G}@oo22bb {C}┃ {R}CH: {G}@SOFESKR{G}""")
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output = render('chek_LV', font='block', colors=['white', 'red'], align='center', space=True)
    print('\033[1m' + output)
    print(f"{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    banner()
print(f"""
    	{W}[{a3}1{W}] {J21}= {a4}Save Acount IN File  {J22} - {RED} حفض النتائج في البوت
    	{W}[{a3}2{W}] {J21}= {a4}Save Acount IN File  {J22} - {RED} حفض النتائج في الملف
    	{W}[{a3}3{W}] {J21}= {a4}All{J22} - {RED} الكل
    """)
dexter = int(input(f'\t{W}[{RED}×{W}] {P2}Enter Number : '))
if dexter == 1:
	BOT_TOKEN = input(f'	{GREEN}Token : ')
	CHAT_ID = input(f'	{GREEN}Id : ')
elif dexter == 2:
	lev = input('	Enter File Path  : ')
else:
	BOT_TOKEN = input(f'	{GREEN}Token : ')
	CHAT_ID = input(f'	{GREEN}Id : ')
	lev = input('	Enter File Path  : ')
os.system('clear')
banner()


# إنشاء البوت
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# عدادات
true_count = 0
false_count = 0
check_count = 0
none_count = 0


async def fetch_user_info(username: str):
    """جلب معلومات المستخدم من تيك توك"""
    try:
        url = f"https://www.tiktok.com/@{username}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.text()

        m = re.search(r'({"__DEFAULT_SCOPE__":.*})</script>', text, re.DOTALL)
        if not m:
            return None

        data = json.loads(m.group(1))
        user = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]
        stats = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["stats"]

        return {
            "id": user.get("id", ""),
            "name": user.get("nickname", ""),
            "username": user.get("uniqueId", ""),
            "bio": user.get("signature", ""),
            "language": user.get("language", ""),
            "private": user.get("secret", False),
            "following": stats.get("followingCount", 0),
            "followers": stats.get("followerCount", 0),
            "likes": stats.get("heartCount", 0),
            "videos": stats.get("videoCount", 0),
        }

    except Exception:
        return None


async def get_level_by_userid(user_id: str):
    """جلب المستوى باستخدام ID المستخدم"""
    try:
        url = "https://webcast16-normal-no1a.tiktokv.eu/webcast/user/"
        params = {
            'device_platform': 'android',
            'ssmix': 'a',
            'channel': 'googleplay',
            'aid': '1233',
            'app_name': 'musical_ly',
            'version_code': '360505',
            'version_name': '36.5.5',
            'manifest_version_code': '2023605050',
            'update_version_code': '2023605050',
            'ab_version': '36.5.5',
            'os_version': '10',
            "device_id": 1234567890,
            'app_version': '30.1.2',
            "request_from": "profile_card_v2",
            "request_from_scene": '1',
            "scene": "1",
            "mix_mode": "1",
            "os_api": "34",
            "ac": "wifi",
            "request_tag_from": "h5",
            "target_uid": str(user_id),
            "device_type": "RMX3511",
            "webcast_sdk_version": "2920",
        }

        params.update(SignerPy.get(params=params))
        sig = SignerPy.sign(params=params)

        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2022703020 (Linux; Android 7.1.2)",
            'x-ss-req-ticket': sig.get('x-ss-req-ticket', ''),
            'x-argus': sig.get('x-argus', ''),
            'x-gorgon': sig.get('x-gorgon', ''),
            'x-khronos': sig.get('x-khronos', ''),
            'x-ladon': sig.get('x-ladon', ''),
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as resp:
                text = await resp.text()

        m = re.search(r'"default_pattern":"(.*?)"', text)
        if not m:
            return None

        pattern = m.group(1)
        return pattern.split('level')[0].strip() if 'level' in pattern else pattern.strip()

    except Exception:
        return None


async def process_username(username: str):
    """معالجة كل اسم مستخدم"""
    global true_count, false_count, check_count, none_count
    check_count += 1

    try:
        user_info = await fetch_user_info(username)
        if not user_info:
            false_count += 1
            print(f"\r	{GREEN}True : {true_count}{RESET}  {RED}False : {false_count}{RESET}  {BLUE}Check : {check_count}{RESET}  None : {none_count}", end="", flush=True)
            bot.send_message(CHAT_ID, f"❌ لم أستطع جلب معلومات @{username}")
            return

        level = await get_level_by_userid(user_info["id"])
        if level:
            true_count += 1
        else:
            false_count += 1

        print(f"\r	{GREEN}True : {true_count}{RESET}  {RED}False : {false_count}{RESET}  {BLUE}Check : {check_count}{RESET}  None : {none_count}", end="", flush=True)

        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"""    
 •-•-•-•-•-•-•-•-•-•-•-•-•-•-•-•       
❄️Level : [ {level if level else "idk"} ]
•-•-•-•-•-•-•-•-•-•-•-•-•-•-•-•
❄️username : {user_info['username']}
❄️email : {user_info['username']}@gmail.com
❄️Followers : {user_info['followers']}
❄️Following : {user_info['following']}
❄️Language : {user_info['language']}
•-•-•-•-•-•-•-•-•-•-•-•-•-•-•-•
        """

        # حفظ النتائج في الملف
        with open(lev, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

        # إرسال النتائج إلى التليجرام
        bot.send_message(CHAT_ID, msg)

    except Exception:
        none_count += 1
        print(f"\r	{GREEN}True : {true_count}{RESET}  {RED}False : {false_count}{RESET}  {BLUE}Check : {check_count}{RESET}  None : {none_count}", end="", flush=True)


async def main():
    os.system('clear')
    banner()
    fileuser = input('Put File Username Path: ')
    os.system('clear')
    banner()
    if not os.path.exists(fileuser):
        print("❌ الملف غير موجود")
        return

    with open(fileuser, "r", encoding="utf-8") as f:
        usernames = [line.strip() for line in f if line.strip()]

    print(f"📂 عدد المستخدمين: {len(usernames)}")
    time.sleep(3)
    os.system('clear')

    for username in usernames:
        await process_username(username)
        await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
