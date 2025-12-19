import requests
import time
import os
import http.server
import socketserver
import threading
import sys
import random

sys.stdout.reconfigure(line_buffering=True)

# --- CONFIGURATION (NAYI ID KI COOKIES UPDATED) ---
COOKIES = "datr=tVYVZWl58HyjpwHKAyi5bw1F; sb=tVYVZYPgZaY6B-uGqpIPoPDm; m_pixel_ratio=2.8125; usida=eyJ2ZXIiOjEsImlkIjoiQXM4dXF5NzFnc2RmamEiLCJ0aW1lIjoxNzA3OTI0NDYzfQ%3D%3D; ps_l=1; ps_n=1; oo=v1; x-referer=eyJyIjoiL2NoZWNrcG9pbnQvMTUwMTA5MjgyMzUyNTI4Mi9sb2dvdXQvP25leHQ9aHR0cHMlM0ElMkYlMkZtLmZhY2Vib29rLmNvbSUyRnVuaWZpZWQlMkZsb2dpbl92aWElMkZhcHAlMkYlM0ZsaWQlM0QwUzdFa3M2Y1RkWUhxaUVKcyUyNmJuJTNEWTI5dExtRnVaSEp2YVdRdVkyaHliMjFsJTI2dGFkZSUzRFE3ZkxCUUdBaElXJTI1MkZmekxDcXV1TWExbThJaXBqUG5SUUJLT2VhOHQxTlZtSmZUWEwlMjUyQnpSWnBhcjEzNVhjaUo3bVlidWNMcm5tOFdWcnJlNExxMyUyNTJCT0tBR1IxSWxDTTdSQ2xRciUyNTJCdVBHNmZ2NjIzb0V3Zk94aHElMjUyQnp5UFFrSzU5NVljcEpMNmxWQzFRJTI1M0QlMjUzRCIsImgiOiIvY2hlY2twb2ludC8xNTAxMDkyODIzNTI1MjgyL2xvZ291dC8%2FbmV4dD1odHRwcyUzQSUyRiUyRm0uZmFjZWJvb2suY29tJTJGdW5pZmllZCUyRmxvZ2luX3ZpYSUyRmFwcCUyRiUzRmxpZCUzRDBTN0VrczZjVGRZSHFpRUpzJTI2Ym4lM0RZMjl0TG1GdVpISnZhV1F1WTJoeWIyMWwlMjZ0YWRlJTNEUTdmTEJRR0FoSVclMjUyRmZ6TENxdXVNYTFtOElpcGpQblJRQktPZWE4dDFOVm1KZlRYTCUyNTJCelJacGFyMTM1WGNpSjdtWWJ1Y0xybm04V1ZycmU0THEzJTI1MkJPS0FHUjFJbENNN1JDbFFyJTI1MkJ1UEc2ZnY2MjNvRXdmT3hocSUyNTJCenlQUWtLNTk1WWNwSkw2bFZDMVElMjUzRCUyNTNEIiwicyI6Im0ifQ%3D%3D; vpd=v1%3B689x384x2.8125; locale=hi_IN; dpr=2.8125; wd=384x857; c_user=100036884583435; xs=46%3A1s26Z_rFkcaTVw%3A2%3A1766135709%3A-1%3A-1; fr=0SVdEJPo1e5ujFfZQ.AWe9QL5JcoDKMMyJoX_TDvbJrgO3Owzo7AlDVxHakYuuNYhqRtE.Bo5U1w..AAA.0.0.BpRRei.AWdAcVjYjxbDMO_I45jxgoKRjSM; pas=100003906934330%3AwgAWalYUmi%2C100004399845208%3ASlIj03v5ES%2C100070692953094%3AutulEWvl7B%2C61572838536475%3AesAhcws6QB%2C100083936531440%3AdsCAwLYyj2%2C100027205080212%3A3kmQgB59wA%2C100044203363472%3AY8tNvAi61q%2C61572564373904%3AHewlnxdrCd%2C100072620126563%3AD9D1jW46LE%2C61573693710968%3ADbz1kJiOzM%2C100044554087935%3A4ASz3G46A1%2C100001743870831%3A79JjzCbEXF%2C61572406665836%3AdZ6bxPs1kz%2C61567710675311%3AFqY4RANRwB%2C100068682382521%3AQE5NjPXdNU%2C100003773046435%3A0aAyf7OTpV%2C61567342787964%3AcSh3N257Bb%2C100023424317842%3AjFRsHd91DA%2C61567875546626%3AeWVslmhg66%2C61568325472223%3ApMLdrFM61s%2C100087327818099%3AZjcBDWWXd1%2C61567829974612%3Ai57UEHR5GJ%2C100054603944602%3AvwqNoO7A8W%2C61568320341249%3ASP7MgpSQWM%2C100089577667420%3AWeagxH3yhn%2C61567845994413%3AWbuJ7tTHVp%2C100083921045165%3A6a8G75UAI5%2C100055824259605%3AhVJqGQdxj4%2C100054350903812%3AK9wTLHgkqa%2C100087460176150%3AAUDkZWgDfF%2C61573400293025%3ARn3htHzMwi%2C61573799214936%3Aa3kHQLBWJH%2C61573296885251%3A0hkUR31kBO%2C61573517840123%3AJ2P2xw5hXB%2C61572877875496%3AQizcEyEHkg%2C100052060385939%3AHyVnd3wpPc%2C61573348106112%3ARDPu0vIV5o%2C100087755821342%3A4IL0mFOySQ%2C61572728625064%3Acek7z9hJHp%2C61573886042952%3AxOEcQcGa81%2C61573677425725%3AsjIQKWRHrV%2C61573316560414%3Acetk1dlYoo%2C61573119009091%3AlB1a7AUzpm%2C100087090830740%3AtUZ9KgzdJl%2C100026185817360%3AK6y4cIK9dY%2C100045192306406%3AfesRdl4ArC%2C100031082015691%3AcsNGRThRe6%2C100076620437000%3AkJhz7qrh8z%2C61573176509790%3AT0ZMIrAyyW%2C100069098898976%3AtdTrsUSlBa%2C100008303177414%3A6qrUUqzugz%2C100069559960225%3ANNze9Dv0Xk%2C100063552933634%3ABehhg4tQbN%2C100036884583435%3A7ob7kIb8mK%2C100075504235837%3AgCCpzVQdf9%2C100029130043949%3ABNrAkxRJE9%2C100063010223024%3AxMRh6IseE2%2C100027988191283%3AHFb6QjxMmo; fbl_st=100722998%3BT%3A29435595; wl_cbv=v2%3Bclient_version%3A3023%3Btimestamp%3A1766135714"
TARGET_ID = "1373445670862571"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"SAFE BOT IS LIVE")

def run_server():
    PORT = int(os.environ.get('PORT', 10000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.serve_forever()

def send_messages():
    print(">> STARTING BOT WITH NEW ID SESSION <<", flush=True)
    try:
        with open('time.txt', 'r') as f: base_delay = int(f.read().strip())
        if base_delay < 60: base_delay = 60 # Safety
        
        with open('haternames.txt', 'r') as f: hater = f.read().strip()
        with open('NP.txt', 'r') as f:
            messages = [m.strip() for m in f.readlines() if m.strip()]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Cookie': COOKIES,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://mbasic.facebook.com'
        }

        while True:
            for i, msg in enumerate(messages):
                url = f"https://mbasic.facebook.com/messages/send/?icm=1"
                payload = {
                    'tids': f'cid.g.{TARGET_ID}',
                    'body': f"{hater} {msg}",
                    'send': 'Send'
                }
                
                response = requests.post(url, data=payload, headers=headers)
                t = time.strftime("%I:%M:%S %p")
                
                if response.status_code == 200:
                    # Logs "DISPATCHED" instead of "SENT" because delivery isn't guaranteed
                    print(f"[{t}] DISPATCHED SUCCESS: {i+1}", flush=True)
                else:
                    print(f"[{t}] FAILED: HTTP {response.status_code}", flush=True)
                
                # Adding random noise to delay to avoid detection
                wait_time = base_delay + random.randint(10, 30)
                print(f"Next message in {wait_time} seconds...", flush=True)
                time.sleep(wait_time)
                
    except Exception as e:
        print(f"FATAL ERROR: {e}", flush=True)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    send_messages()
