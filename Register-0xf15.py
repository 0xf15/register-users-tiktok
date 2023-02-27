import os
import ctypes

import random
import string
from threading import Thread, Lock
from time import sleep
import time
from colorama import Fore, init, Style
import pycurl
import ctypes
import random
import json
from threading import Thread

from requests import get, post

from utils import Captcha
from utils import Utils
file_proxy = []
for i in open('proxy.txt').read().splitlines():
    if (":" in i):
        file_proxy.append(i)
init()


class Auto():
    def __init__(self):
        self.rs = 0
        self.att = 0
        self.errors = 0
        self.secend = 0
        self.dd = ""
        pass

    

    def SendRequest2(self, user,pwd, httpClient, proxy, ms):

        d = ''.join(random.choices(string.digits, k=18))
        
        if (Captcha(did=d, iid=0).solve_captcha()["code"] == 200):

            httpClient.setopt(
                pycurl.URL, f'https://api22-normal-c-useast1a.tiktokv.com/passport/web/username/register/?aid=14591&device_id={d}&account_sdk_source=web&language=ar&shark_extra=%7B%22aid%22:1459,%22app_name%22:%22Tik_Tok_Login%22,%22channel%22:%22tiktok_web%22,%22device_platform%22:%22web_pc%22,%22device_id%22:%22{d}%22,%22region%22:%22SA%22,%22priority_region%22:%22%22,%22os%22:%22windows%22,%22referer%22:%22https:%2F%2Fwww.tiktok.com%2Flogout%3Fredirect_url%3Dhttps%253A%252F%252Fwww.tiktok.com%252F%2540sxsacvx9xx2s21af%22,%22root_referer%22:%22https:%2F%2Fwww.tiktok.com%2F%40kdasdk%22,%22cookie_enabled%22:true,%22screen_width%22:1920,%22screen_height%22:1080,%22browser_language%22:%22ar%22,%22browser_platform%22:%22Win32%22,%22browser_name%22:%22Mozilla%22,%22browser_version%22:%225.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML,+like+Gecko)+Chrome%2F110.0.0.0+Safari%2F537.36%22,%22browser_online%22:true,%22verifyFp%22:%22verify_leek8uv3_3PcL5kTB_AI71_4fOX_Anuh_W5QcaY273b2P%22,%22app_language%22:%22ar%22,%22webcast_language%22:%22ar%22,%22tz_name%22:%22Asia%2FRiyadh%22,%22is_page_visible%22:true,%22focus_state%22:true,%22is_fullscreen%22:false,%22history_len%22:19,%22battery_info%22:null%7D&msToken={ms}&X-Bogus=DFSzswVLL{d}&_signature=f15dv')
            httpClient.setopt(pycurl.SSL_VERIFYPEER, 0)
            httpClient.setopt(pycurl.SSL_VERIFYHOST, 0)
            httpClient.setopt(pycurl.NOSIGNAL, 10)
            httpClient.setopt(pycurl.TIMEOUT, 5)
            httpClient.setopt(pycurl.PROXY, str(proxy).split(':')[0])
            httpClient.setopt(pycurl.CUSTOMREQUEST, 'POST')
            httpClient.setopt(
                pycurl.POSTFIELDS, f"mix_mode=1&password={pwd}&aid=1459&account_sdk_source=app&language=en&birthday=1986-01-02&username={user}")
            httpClient.setopt(pycurl.PROXYPORT, int(str(proxy).split(':')[1]))
            httpClient.setopt(pycurl.PROXYTYPE, 1)

            httpClient.setopt(pycurl.HTTPHEADER, [
               
                'Content-Type: application/x-www-form-urlencoded',
                "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
                "Referer: https://www.tiktok.com/"

            ])
            return httpClient.perform_rs()
        else:
            return False

    def Reg(self, user,pwd, httpClient, proxy, ms):
        try:

            try:

                req = self.SendRequest2(user,pwd, httpClient, proxy, ms)

            except:
                return False
            if ("user_id" in req):
                self.att += 1
                return req
            elif ("The name already exists" in req):

               
                return False
            else:
               
                self.errors += 1
                return False
        except:
            return False
        
    def get_ms_token(self,proxy):
        url = "https://mssdk-va.tiktok.com/web/report"
        headers = {
        
            "Sec-Ch-Ua": """Chromium"";v=""110"", ""Not A(Brand"";v=""24"", ""Google Chrome"";v=""110""",
            "Sec-Ch-Ua-Platform": """Windows""",
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "Content-Type": "text/plain;charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://www.tiktok.com",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.tiktok.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
            "Connection": "close",
        }
        jso = {"magic": 538969122, "version": 1, "dataType": 8, "strData": "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", "tspFromClient": 1677004216767}

        req = post(url, headers=headers, json=jso, proxies={
                "http": proxy, "https": proxy}, timeout=4)
        return req.cookies["msToken"]
        
    def save(self,user,pwd,reg):

        session_key = json.loads(reg)["data"]["session_key"]

        post("https://api16-normal-c-alisg.tiktokv.com/aweme/v3/user/info/sync/?residence=SA&device_id=7170477432607278598&os_version=14.4&iid=7177441455559886598&app_name=musical_ly&locale=en&ac=WIFI&sys_region=SA&js_sdk_version=1.77.0.2&version_code=21.1.0&channel=App%20Store&vid=7094F26A-EC10-45E4-8854-5D0616167B08&op_region=SA&tma_jssdk_version=1.77.0.2&os_api=18&idfa=D2CF453D-6981-4F32-A0EB-7A200FED8504&device_platform=ipad&device_type=iPad11,6&openudid=3d06da82ad99a50a90dce612cb54d7e456bf69b4&account_region=&tz_name=Asia/Riyadh&tz_offset=10800&app_language=en&current_region=SA&build_number=211023&aid=1233&mcc_mnc=&screen_width=1620&uoo=1&content_language=&language=en&cdid=5C549689-6EC2-4C06-9D19-0009B844A7A6&app_version=21.1.0", headers={

            'Cookie': f'sessionid={session_key}',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'TikTok 21.1.0 rv:211023 (iPad; iOS 14.4; en_SA@calendar=gregorian) Cronet',
            'Sdk-Version': '2'
        }, data="birthday=1995-12-15").text

        print(
            f"Done Registered @{user} || Password: {pwd} || Session_key: {session_key}")
        with open("goods.txt", "a") as myfile:
            myfile.write(
                f"@{user} || Password: {pwd} || Session_key: {session_key}\n")
tik = Auto()


def calc():
    while True:


            tik.secend = tik.att
            time.sleep(1)
            tik.rs = tik.att - tik.secend
            
            print("\r{}{}{}kali@F15dv{}:{}~{}$ Done: {}{:,}{} || R/S: {}{:,}{}".format(Style.BRIGHT, Fore.WHITE,
                                                                  Fore.GREEN, Fore.WHITE, Fore.BLUE, Fore.WHITE,Fore.MAGENTA, tik.att,Fore.WHITE,Fore.MAGENTA,tik.rs,Fore.WHITE), end="\r")


def main():
    httpClient = pycurl.Curl()
    while True:
        try:

            user = ''.join(random.choices(
                "1234567890_.qwertyuipolkjhgfdsazmxncbv", k=8))
            proxy = random.choice(file_proxy)
            pwd =''.join(random.choices(
                "qwertyuipolkjhgfdsazmxncbv", k=8))+"@#F15dv"
            ms = tik.get_ms_token(proxy)
            reg = tik.Reg(user,pwd, httpClient, proxy, ms)
            if (reg == False):
                pass
            else:
                tik.save(user,pwd, reg)
        except:
            pass


print("\r{}{}{}kali@F15dv{}:{}~{}$ Threads: ".format(Style.BRIGHT, Fore.WHITE,
                                                                  Fore.GREEN, Fore.WHITE, Fore.BLUE, Fore.WHITE), end="")
Threads = int(input())
print("Tele - @f15dv")
input()
os.system('cls' if os.name == 'nt' else 'clear')
Thread(target=calc).start()
for i in range(Threads):
    try:
        Thread(target=main).start()
    except:
        Thread(target=main).start()
