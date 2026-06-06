import unittest
from src.core.crypto.secret_sharing import SecretSharing

class TestSecretSharing(unittest.TestCase):
    def test_split_and_recover_success(self):
        secret = b"ProductionKey2026"
        length = len(secret)
        shares = SecretSharing.split_secret(secret, 3, 5)
        self.assertEqual(len(shares), 5)
        
        recovered = SecretSharing.recover_secret(shares[:3], length)
        self.assertEqual(recovered, secret)
        
        recovered_all = SecretSharing.recover_secret(shares, length)
        self.assertEqual(recovered_all, secret)

    def test_insufficient_shares_logic(self):
        # We expect that providing insufficient shares will recover the WRONG secret, 
        # but not necessarily throw a Python OverflowError.
        secret = b"Secret"
        shares = SecretSharing.split_secret(secret, 3, 5)
        recovered = SecretSharing.recover_secret(shares[:2], len(secret))
        self.assertNotEqual(recovered, secret)

    def test_invalid_threshold(self):
        with self.assertRaises(ValueError):
            SecretSharing.split_secret(b"test", 5, 3)

if __name__ == "__main__":
    unittest.main()
