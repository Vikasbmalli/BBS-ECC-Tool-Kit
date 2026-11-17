"""ECC ECDH key agreement + HKDF + AES-GCM demonstration.

Uses the maintained 'cryptography' package rather than implementing
elliptic-curve arithmetic manually.
"""

import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_aes_key(shared_secret: bytes, salt: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"BCS703-ECC-ECDH-demo",
    ).derive(shared_secret)


def public_key_pem(public_key) -> bytes:
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def run_demo(message: str):
    # Alice and Bob independently generate P-256 elliptic-curve key pairs.
    alice_private = ec.generate_private_key(ec.SECP256R1())
    bob_private = ec.generate_private_key(ec.SECP256R1())
    alice_public = alice_private.public_key()
    bob_public = bob_private.public_key()

    # ECDH: each side combines its private key with the other side's public key.
    alice_shared = alice_private.exchange(ec.ECDH(), bob_public)
    bob_shared = bob_private.exchange(ec.ECDH(), alice_public)

    if alice_shared != bob_shared:
        raise RuntimeError("ECDH shared secrets do not match.")

    salt = os.urandom(16)
    aes_key = derive_aes_key(alice_shared, salt)

    # AES-GCM encrypts and authenticates the message using the derived key.
    nonce = os.urandom(12)
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, message.encode("utf-8"), None)
    decrypted = aesgcm.decrypt(nonce, ciphertext, None).decode("utf-8")

    print("\n=== ECC / ECDH Demonstration ===")
    print("Curve: NIST P-256 (SECP256R1)")
    print("\nAlice public key (PEM):")
    print(public_key_pem(alice_public).decode("ascii"))
    print("Bob public key (PEM):")
    print(public_key_pem(bob_public).decode("ascii"))
    print("ECDH shared secrets match:", alice_shared == bob_shared)
    print("Derived AES key length:", len(aes_key), "bytes")
    print("\nOriginal message:", message)
    print("Encrypted data (hex):", ciphertext.hex())
    print("Decrypted message:", decrypted)
    print("Decryption successful:", decrypted == message)


def main():
    print("ECC ECDH + AES-GCM secure communication demo")
    message = input("Enter a message to encrypt: ").strip()
    if not message:
        message = "Hello! This is an ECC encrypted message."
    run_demo(message)


if __name__ == "__main__":
    main()
