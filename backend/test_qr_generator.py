import unittest

from backend.qr_generator import build_table_qr_url


class QrGeneratorUrlTest(unittest.TestCase):
    def test_builds_frontend_menu_url(self):
        url = build_table_qr_url("abc123", restaurant_id=1, table_number=4)

        self.assertIn("frontend/menu.html", url)
        self.assertIn("token=abc123", url)
        self.assertNotIn("/menu?token=", url)


if __name__ == "__main__":
    unittest.main()
