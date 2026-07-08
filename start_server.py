import http.server
import socket
import socketserver
import webbrowser
import os
import sys
import subprocess
from pathlib import Path

PORT = 8000

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def ensure_qrcode():
    try:
        import qrcode
        from PIL import Image
        return qrcode
    except Exception:
        print("Dang cai thu vien tao QR... Neu may hoi, hay cho phep.")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "qrcode[pil]"])
        import qrcode
        return qrcode

os.chdir(Path(__file__).parent)
ip = get_lan_ip()
url = f"http://{ip}:{PORT}/index.html"

try:
    qrcode = ensure_qrcode()
    img = qrcode.make(url)
    qr_path = Path("QR_QUET_DE_VAO_WEB.png")
    img.save(qr_path)
    print("\nDA TAO MA QR THAT:")
    print(qr_path.resolve())
    try:
        os.startfile(qr_path.resolve())
    except Exception:
        pass
except Exception as e:
    print("\nKhong tao duoc anh QR tu dong.")
    print("Ban van co the copy link nay de tao QR:", url)
    print("Loi:", e)

print("\nWEB DANG CHAY TAI:")
print(url)
print("\nDien thoai va may tinh phai dung chung Wi-Fi.")
print("Dung cua so nay khi ban muon tat web.")
print("Neu khong vao duoc, hay cho phep Python qua Windows Firewall.\n")

webbrowser.open(url)

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
