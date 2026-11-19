import unittest

import app as demo


class App(unittest.TestCase):
    def setUp(self):
        demo.entries.clear()
        self.c = demo.app.test_client()

    def test_health(self):
        self.assertEqual(self.c.get("/healthz").status_code, 200)

    def test_sign_and_list(self):
        r = self.c.post("/sign", data={"name": "ada", "message": "hello"})
        self.assertEqual(r.status_code, 302)
        page = self.c.get("/").get_data(as_text=True)
        self.assertIn("ada", page)
        self.assertIn("hello", page)

    def test_messages_are_escaped(self):
        self.c.post("/sign", data={"name": "x", "message": "<script>alert(1)</script>"})
        page = self.c.get("/").get_data(as_text=True)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_empty_message_ignored(self):
        self.c.post("/sign", data={"name": "x", "message": "  "})
        self.assertEqual(demo.entries, [])

    def test_info(self):
        self.assertEqual(self.c.get("/api/info").get_json()["app"], "demo")


if __name__ == "__main__":
    unittest.main()
