# Plan — Issue #41: add a hello endpoint

Python 3 standard library only. Two files at the repo root: `hello.py`,
`test_hello.py`. Nothing else changes.

## Step 1 — Write the failing test (`test_hello.py`)

One `unittest.TestCase` with one test method, `test_get_hello`:

- `setUp`: `self.server = hello.make_server("127.0.0.1", 0)`; start
  `self.server.serve_forever` in a `threading.Thread(daemon=True)`.
- `tearDown`: `self.server.shutdown()`; `self.server.server_close()`.
- Test: use `http.client.HTTPConnection("127.0.0.1", port, timeout=5)` where
  `port = self.server.server_address[1]`; `GET /hello`; assert
  - `response.status == 200`
  - `response.getheader("Content-Type") == "text/plain"`
  - `response.read() == b"hello"`

**Proof:** `python3 -m unittest test_hello -v` fails (ImportError / missing
`make_server`) before Step 2.

## Step 2 — Implement the server (`hello.py`)

- `class HelloHandler(http.server.BaseHTTPRequestHandler)` with `do_GET`:
  - if `self.path == "/hello"`: `send_response(200)`,
    `send_header("Content-Type", "text/plain")`,
    `send_header("Content-Length", "5")`, `end_headers()`,
    `wfile.write(b"hello")`.
  - otherwise: `self.send_error(404)`.
- `def make_server(host="127.0.0.1", port=8000)` returns
  `http.server.HTTPServer((host, port), HelloHandler)`.
- `if __name__ == "__main__":` read optional port from `sys.argv[1]`
  (default `8000`), build the server, print the URL, `serve_forever()`;
  close the server on `KeyboardInterrupt`.

**Proof:** `python3 -m unittest test_hello -v` passes (1 test, OK).

## Step 3 — Manual smoke check

Run `python3 hello.py` and `curl -i http://127.0.0.1:8000/hello`.

**Proof:** response shows `HTTP/1.0 200 OK`, `Content-Type: text/plain`, body
`hello`. (Covered step by step in `uat.md`.)

## Step 4 — Scope check

`git status` shows only `hello.py` and `test_hello.py` as new files (plus the
spec docs already in `docs/specs/41/`).

**Proof:** no other paths in the diff; no protected path touched.
