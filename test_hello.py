import http.client
import threading
import unittest

import hello


class HelloTest(unittest.TestCase):
    def setUp(self):
        self.server = hello.make_server("127.0.0.1", 0)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_get_hello(self):
        port = self.server.server_address[1]
        conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            conn.request("GET", "/hello")
            response = conn.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(response.getheader("Content-Type"), "text/plain")
            self.assertEqual(response.read(), b"hello")
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
