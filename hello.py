import http.server
import sys


class HelloHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/hello":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", "5")
            self.end_headers()
            self.wfile.write(b"hello")
        else:
            self.send_error(404)


def make_server(host="127.0.0.1", port=8000):
    return http.server.HTTPServer((host, port), HelloHandler)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = make_server(port=port)
    print(f"Serving on http://127.0.0.1:{port}/hello")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
