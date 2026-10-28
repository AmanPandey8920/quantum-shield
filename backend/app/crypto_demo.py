from __future__ import annotations

from cryptography.hazmat.primitives.asymmetric import mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class MLKEMAESDemo:
    def __init__(self) -> None:
        self.private_key = mlkem.MLKEM768PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def establish_shared_secret(self) -> tuple[bytes, bytes]:
        shared_secret, ciphertext = self.public_key.encapsulate()
        decapsulated = self.private_key.decapsulate(ciphertext)
        return shared_secret, decapsulated

    def encrypt_payload(self, plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
        aesgcm = AESGCM(key)
        nonce = b"\x00" * 12
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return nonce, ciphertext

    def decrypt_payload(self, nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
        aesgcm = AESGCM(key)
        return aesgcm.decrypt(nonce, ciphertext, None)

    def tamper_detection(self, plaintext: bytes) -> tuple[bytes, bytes]:
        key = b"\x11" * 32
        nonce, ciphertext = self.encrypt_payload(plaintext, key)
        tampered = bytearray(ciphertext)
        tampered[-1] ^= 0xFF
        return nonce, bytes(tampered)
