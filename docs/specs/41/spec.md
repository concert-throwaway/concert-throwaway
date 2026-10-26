# Spec — Issue #41: add a hello endpoint

## Summary

Add a minimal HTTP server, written with the Python 3 standard library only
(`http.server`), that answers `GET /hello` with the plain-text body `hello`.

## What changes for users

- A new file `hello.py` at the repository root. Running it starts an HTTP server.
- `GET /hello` returns:
  - status `200 OK`
  - header `Content-Type: text/plain`
  - body exactly `hello` (5 bytes, no trailing newline).
- A new file `test_hello.py` at the repository root with one `unittest` test
  that proves the behaviour above.

## What does not change

- No other files are added or modified (no README edit, no config, no
  dependencies, no `requirements.txt`, no CI changes).
- No third-party packages; standard library only.
- Paths other than `/hello` and methods other than `GET` are not part of this
  change. They keep `http.server`'s default behaviour (e.g. `404` for unknown
  paths via `send_error`, `501` for unsupported methods).
- There is no earlier "Stage 1" to depend on; this is the first app code in the repo.

## Design notes

- `hello.py` defines a `BaseHTTPRequestHandler` subclass (`HelloHandler`) with
  `do_GET`, plus a small `make_server(host, port)` helper and a
  `if __name__ == "__main__":` block that serves forever.
- Default bind: `127.0.0.1`, port `8000`; overridable by an optional port
  argument on the command line (`python3 hello.py 8080`). Binding to localhost
  by default avoids exposing the server on all interfaces.
- `Content-Length: 5` is sent so clients know the body is complete.

## Risks

- **CI does not run the test.** `process.yaml` sets `ci.local.tests` to
  `echo tests ok`, and `process.yaml`/`.github/**` are protected paths that this
  change must not touch. The unittest therefore has to be run by hand (see
  `uat.md`); CI green does not prove the endpoint works.
- **Port collisions in tests.** Mitigated by binding the test server to port
  `0` (OS-assigned free port).
- **Test hangs.** Mitigated by running the server in a daemon thread and
  calling `shutdown()`/`server_close()` in teardown, with a client timeout.

## Open questions

None blocking. Decided by the project's humans: stdlib only, `hello.py` at the
root, body exactly `hello`, `Content-Type: text/plain`, one unittest in
`test_hello.py`, no other files.
