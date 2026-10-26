"""
Sadə Fayl Paylaşma Serveri
===========================
Yalnız Python-un standart kitabxanası (http.server) istifadə olunur.
Flask YOXDUR - bu bilərəkdən belədir, əvvəlcə HTTP-nin özünü anlamaq üçün.

İşə salmaq:
    python3 server.py

Sonra brauzerdə:
    http://<server-in-IP-si>:8000

QEYD: Bu kodun hər hissəsi dərslərdə ayrı-ayrı izah ediləcək.
İndi sadəcə "işləyən" versiyadır - "anlaşılan" versiya deyil hələ.
"""

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote
import html

# Faylların saxlanacağı qovluq
STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shared_files")
PORT = 8000

# Qovluq yoxdursa yarat
os.makedirs(STORAGE_DIR, exist_ok=True)


class FileServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.show_file_list()
        elif self.path.startswith("/download/"):
            self.send_file()
        else:
            self.send_error(404, "Tapilmadi")

    def do_POST(self):
        if self.path == "/upload":
            self.handle_upload()
        else:
            self.send_error(404, "Tapilmadi")

    # ---------- Fayl siyahisi ve HTML sehife ----------

    def show_file_list(self):
        files = sorted(os.listdir(STORAGE_DIR))

        rows = ""
        if not files:
            rows = "<p>Hele hec bir fayl yoxdur.</p>"
        else:
            for name in files:
                safe_name = html.escape(name)
                rows += f'<li><a href="/download/{safe_name}">{safe_name}</a></li>\n'

        page = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>Home Server - Fayllar</title>
            <style>
                body {{ font-family: sans-serif; max-width: 600px; margin: 40px auto; }}
                li {{ margin: 8px 0; }}
            </style>
        </head>
        <body>
            <h1>Fayllar</h1>
            <ul>
                {rows}
            </ul>
            <hr>
            <h2>Yukle</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Yukle">
            </form>
        </body>
        </html>
        """
        body = page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ---------- Fayl endirme ----------

    def send_file(self):
        filename = unquote(self.path[len("/download/"):])
        filepath = os.path.join(STORAGE_DIR, filename)

        # Tehlukesizlik: qovluqdan kenara cixmagin qarsisini al
        if not os.path.abspath(filepath).startswith(os.path.abspath(STORAGE_DIR)):
            self.send_error(403, "Qadagandir")
            return

        if not os.path.isfile(filepath):
            self.send_error(404, "Fayl tapilmadi")
            return

        with open(filepath, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # ---------- Fayl yukleme ----------

    def handle_upload(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self.send_error(400, "Multipart gozlenilirdi")
            return

        boundary = content_type.split("boundary=")[-1].encode()
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        parts = body.split(b"--" + boundary)

        saved_name = None
        for part in parts:
            if b"filename=" not in part:
                continue

            header_end = part.find(b"\r\n\r\n")
            if header_end == -1:
                continue

            headers_part = part[:header_end].decode(errors="ignore")
            file_data = part[header_end + 4:]
            # son CRLF-i at
            if file_data.endswith(b"\r\n"):
                file_data = file_data[:-2]

            filename = None
            for line in headers_part.split("\r\n"):
                if "filename=" in line:
                    filename = line.split("filename=")[-1].strip('"')

            if filename:
                safe_name = os.path.basename(filename)
                save_path = os.path.join(STORAGE_DIR, safe_name)
                with open(save_path, "wb") as f:
                    f.write(file_data)
                saved_name = safe_name

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), FileServerHandler)
    print(f"Server islemeye basladi: http://0.0.0.0:{PORT}")
    print(f"Fayllar bu qovluqda saxlanilir: {STORAGE_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer dayandirildi.")
