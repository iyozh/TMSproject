import socketserver
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs

year = datetime.now().year
hour = datetime.now().hour

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/goodbye"):
            return self.goodbye_start_response()
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def goodbye_start_response(self):
        if self.path.startswith("/goodbye?") or self.path.startswith("/goodbye/?"):
            arguments = self.parse_function()
            path = self.path_calculating()
            name = arguments.get("name", "anonymous")
            age = int(arguments.get("age", "0"))
            msg = f"""
                                    Hello {name}!                

                                    Your path: {path}

                                                       """
            self.msg_processing(msg, name, path, age)
        else:
            return self.lack_of_qs()

    def msg_processing(self, msg, name, path, age):

        if 'age':
            born = year - age
            msg += f"\n\t\t\t\t   You were born in {born}"
        if hour in range(6, 11):
            msg += f"\n\t\t\t\t   Good morning!"
        elif hour in range(12, 24):
            msg += f"\n\t\t\t\t   Good day!"
        else:
            msg += f"\n\t\t\t\t   Good night!"

        self.response(msg)


    def path_calculating(self):
        if self.path.startswith("/hello/"):
            path = "/goodbye/"
        else:
            path = "/goodbye"

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
