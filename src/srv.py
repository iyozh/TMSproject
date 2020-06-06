import socketserver
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs

year = datetime.now().year

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/hello/?"):
            path, qs = self.path.split("?")
            qs = parse_qs(qs)
            if 'name' not in qs:
                name = 'anonymous'
            else:
                name = qs['name'][0]
            if 'age' in qs:
                age = qs['age'][0]
                born = year - int(age)
                msg = f"""
                        Hello {name}!
                                        
                        You were born in {born} year                    
                                            
                        Your path: {path}
                               """
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.send_header("Content-length", len(msg))
                self.end_headers()

                self.wfile.write(msg.encode())
            msg = f"""
                        Hello {name}!
    
                        Your path: {path}
                """
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(msg))
            self.end_headers()

            self.wfile.write(msg.encode())
        elif self.path.startswith("/hello"):
            msg = f"""
                        Hello anonymous!

                        Your path: {self.path}
                            """
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.send_header("Content-length", len(msg))
            self.end_headers()

            self.wfile.write(msg.encode())
        else:
            return SimpleHTTPRequestHandler.do_GET(self)


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()