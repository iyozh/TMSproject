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
        if self.path.startswith("/hello"):
            return self.hello_start_response()
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def hello_start_response(self):
        if self.path.startswith("/hello?") or self.path.startswith("/hello/?"):
            arguments = self.parse_function()
            path = self.path_calculating()
            name = arguments.get("name", "anonymous")
            age = int(arguments.get("age", "0"))
            msg = f"""
                                   Hello {name}!                

                                   Your path: {path}
            
                                          """
            if 'age':
                born = year - age
                msg += f"\n\t\t\t\t   You were born in {born}"
            self.response(msg)
        else:
            return self.lack_of_qs()

    def path_calculating(self):
        if self.path.startswith("/hello/"):
            path = "/hello/"
        else:
            path = "/hello"

        return path

    def lack_of_qs(self):
        path = self.path_calculating()
        msg = f"""
                                                     Hello anonymous!                

                                                     Your path: {path}

                                                            """
        self.response(msg)

    def parse_function(self):
        path, qs = self.path.split("?")
        arguments = {}
        qs = parse_qs(qs)
        if 'name' in qs:
            name = qs['name'][0]
        for keys, values in qs.items():
            if not values:
                continue
            arguments[keys] = values[0]

        return arguments

    def response(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", len(msg))
        self.end_headers()

        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()
