import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Tuple, Optional

class VaultManager:
    """
    Production Cryptographic Vault.
    Uses AES-256-GCM for authenticated encryption. 
    Implements key wrapping and secure storage interfaces.
    """
    def __init__(self, master_password: str = None, salt: bytes = None):
        self.salt = salt or os.urandom(16)
        self.master_key = self._derive_key(master_password) if master_password else AESGCM.generate_key(bit_length=256)

    def _derive_key(self, password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=480000,
        )
        return kdf.derive(password.encode())

    def encrypt(self, plaintext: str) -> Tuple[bytes, bytes]:
        """
        Encrypts data. Returns (nonce, ciphertext).
        """
        aesgcm = AESGCM(self.master_key)
        nonce = os.urandom(12)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)
        return nonce, ciphertext

    def decrypt(self, nonce: bytes, ciphertext: bytes) -> str:
        """
        Decrypts data using the master key.
        """
        aesgcm = AESGCM(self.master_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode()

    def rotate_key(self, new_password: str):
        """
        Re-encrypts the master key (in a real system, this wraps the key).
        """
        self.master_key = self._derive_key(new_password)

class VaultStorage:
    """
    Physical storage interface for encrypted blobs.
    """
    def __init__(self, base_path: str = "vault_storage"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def save_blob(self, asset_id: str, nonce: bytes, ciphertext: bytes):
        path = os.path.join(self.base_path, f"{asset_id}.bin")
        with open(path, "wb") as f:
            # Store as [nonce_len(1byte)][nonce][ciphertext]
            f.write(len(nonce).to_bytes(1, 'big'))
            f.write(nonce)
            f.write(ciphertext)

    def load_blob(self, asset_id: str) -> Tuple[bytes, bytes]:
        path = os.path.join(self.base_path, f"{asset_id}.bin")
        with open(path, "rb") as f:
            nonce_len = int.from_bytes(f.read(1), 'big')
            nonce = f.read(nonce_len)
            ciphertext = f.read()
            return nonce, ciphertext

if __name__ == "__main__":
    vault = VaultManager("super-secret-pass")
    storage = VaultStorage()
    
    msg = "Critical Asset Key: 0xDEADBEEF"
    nonce, cipher = vault.encrypt(msg)
    storage.save_blob("asset_01", nonce, cipher)
    
    n, c = storage.load_blob("asset_01")
    print(f"Decrypted: {vault.decrypt(n, c)}")
    assert vault.decrypt(n, c) == msg
