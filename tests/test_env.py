import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import unittest
import typot.env as env


class TestEnv(unittest.TestCase):

    def test_private_key(self):
        key = env.get_private_key()
        self.assertTrue(key)

    def test_client_id_secret(self):
        client_id = env.get_client_id()
        client_secret = env.get_client_secret()
        self.assertTrue(client_id)
        self.assertTrue(client_secret)


if __name__ == "__main__":
    unittest.main()
