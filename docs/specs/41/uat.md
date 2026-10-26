# UAT — Issue #41: add a hello endpoint

Prerequisites: Python 3 and `curl` installed; a terminal open at the repo root.

## AC1 — The automated test passes

1. Run `python3 -m unittest test_hello -v`.
2. Expected: one test runs and the output ends with `OK`.

## AC2 — `GET /hello` returns `hello` as plain text

1. In terminal A, run `python3 hello.py`. It keeps running.
2. In terminal B, run `curl -i http://127.0.0.1:8000/hello`.
3. Expected:
   - the first line contains `200 OK`;
   - there is a header `Content-Type: text/plain`;
   - the body is exactly `hello` (no extra text).
4. Optional exact-body check: `curl -s http://127.0.0.1:8000/hello | od -c`
   shows exactly `h e l l o` and nothing after it.

## AC3 — Other paths are not served as hello

1. With the server still running, run `curl -i http://127.0.0.1:8000/other`.
2. Expected: status `404`, and the body is not `hello`.

## AC4 — Custom port works

1. Stop the server in terminal A with Ctrl+C.
2. Run `python3 hello.py 8081`.
3. In terminal B, run `curl -s http://127.0.0.1:8081/hello`.
4. Expected: prints `hello`. Stop the server with Ctrl+C; it exits cleanly.

## AC5 — Nothing else changed

1. Look at the change's file list (PR "Files changed" or `git status`).
2. Expected: only `hello.py`, `test_hello.py`, and the files under
   `docs/specs/41/` are added. No other file is changed, and no third-party
   dependency is added.
