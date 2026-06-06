import unittest
import os
from src.core.crypto.vault import VaultManager, VaultStorage

class TestVault(unittest.TestCase):
    def setUp(self):
        self.password = "master-password-123"
        self.vault = VaultManager(self.password)
        self.storage = VaultStorage("test_vault_data")

    def tearDown(self):
        # Clean up test directory
        import shutil
        if os.path.exists("test_vault_data"):
            shutil.rmtree("test_vault_data")

    def test_encrypt_decrypt_cycle(self):
        msg = "Sensitive Data 123"
        nonce, cipher = self.vault.encrypt(msg)
        decrypted = self.vault.decrypt(nonce, cipher)
        self.assertEqual(msg, decrypted)

    def test_storage_cycle(self):
        msg = "Stored Secret"
        nonce, cipher = self.vault.encrypt(msg)
        self.storage.save_blob("asset_test", nonce, cipher)
        
        n, c = self.storage.load_blob("asset_test")
        self.assertEqual(msg, self.vault.decrypt(n, c))

    def test_wrong_password(self):
        msg = "Secret"
        nonce, cipher = self.vault.encrypt(msg)
        
        wrong_vault = VaultManager("wrong-password")
        with self.assertRaises(Exception): # AESGCM raises InvalidTag
            wrong_vault.decrypt(nonce, cipher)

if __name__ == "__main__":
    unittest.main()
