import requests
import time
import os
import http.server
import socketserver
import threading
import sys

sys.stdout.reconfigure(line_buffering=True)

# --- CONFIGURATION (FRESH COOKIES UPDATED) ---
COOKIES = "datr=tVYVZWl58HyjpwHKAyi5bw1F; sb=tVYVZYPgZaY6B-uGqpIPoPDm; m_pixel_ratio=2.8125; usida=eyJ2ZXIiOjEsImlkIjoiQXM4dXF5NzFnc2RmamEiLCJ0aW1lIjoxNzA3OTI0NDYzfQ%3D%3D; ps_l=1; ps_n=1; oo=v1; pas=100070692953094%3AutulEWvl7B; vpd=v1%3B689x384x2.8125; c_user=100070692953094; xs=32%3ApZbh2vQv2KeLhQ%3A2%3A1766086550%3A-1%3A-1; locale=hi_IN; dpr=2.8125; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1766097614375%2C%22v%22%3A1%7D; wd=924x1658; fr=0SVdEJPo1e5ujFfZQ.AWdRJDCq3mOgb36TAa7bfxjVa3-LbKkq2VnXCzeTqYy-p6PFB1Q.Bo5U1w..AAA.0.0.BpRQzH.AWd_Qo2MI51CjwsHi0gP2bpfUfU; fbl_st=101037190%3BT%3A29434841; wl_cbv=v2%3Bclient_version%3A3023%3Btimestamp%3A1766132935"
TARGET_ID = "1373445670862571"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"MESSENGER BOT IS LIVE")

def run_server():
    PORT = int(os.environ.get('PORT', 10000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.serve_forever()

def send_messages():
    print(">> STARTING BOT WITH FRESH COOKIES <<", flush=True)
    try:
        with open('time.txt', 'r') as f: delay = int(f.read().strip())
        with open('haternames.txt', 'r') as f: hater = f.read().strip()
        with open('NP.txt', 'r') as f:
            messages = [m.strip() for m in f.readlines() if m.strip()]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
            'Cookie': COOKIES,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://mbasic.facebook.com',
            'Referer': f'https://mbasic.facebook.com/messages/read/?tid=cid.g.{TARGET_ID}',
            'Upgrade-Insecure-Requests': '1'
        }

        while True:
            for i, msg in enumerate(messages):
                # Using mbasic for high success rate
                url = f"https://mbasic.facebook.com/messages/send/?icm=1"
                
                payload = {
                    'tids': f'cid.g.{TARGET_ID}',
                    'body': f"{hater} {msg}",
                    'send': 'Send'
                }
                
                response = requests.post(url, data=payload, headers=headers)
                t = time.strftime("%I:%M:%S %p")
                
                # Verify if it actually sent by checking status
                if response.status_code == 200:
                    print(f"[{t}] SENT SUCCESS: {i+1} ({hater})", flush=True)
                else:
                    print(f"[{t}] FAILED: HTTP {response.status_code}", flush=True)
                
                time.sleep(delay)
    except Exception as e:
        print(f"FATAL ERROR: {e}", flush=True)

if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    send_messages()
