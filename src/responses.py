def respond_200(server, msg, content_type):
    response(server, msg, 200, content_type)


def respond_302(server, redirect, cookie):
    response(server, "", 302, "text/plain", redirect, cookie)


def respond_400(server, msg="You miss something..."):
    response(server, msg, 400, "text/plain")


def respond_404(server, msg, content_type):
    response(server, msg, 404, content_type)


def response(
    server, msg, status_code, content_type="text/plain", redirect="", cookie=""
):
    print(cookie)
    server.send_response(status_code)
    server.send_header("Content-type", content_type)
    server.send_header("Content-length", str(len(msg)))
    server.send_header("Location", redirect)
    server.send_header("Set-Cookie", cookie)
    server.end_headers()

    if isinstance(msg, str):
        msg = msg.encode()
    server.wfile.write(msg)
