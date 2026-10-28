from backend.app.crypto_demo import MLKEMAESDemo


def main() -> None:
    demo = MLKEMAESDemo()
    shared_secret_a, shared_secret_b = demo.establish_shared_secret()
    plaintext = b"QuantumShield demo payload"
    key = shared_secret_a[:32]
    nonce, ciphertext = demo.encrypt_payload(plaintext, key)
    decrypted = demo.decrypt_payload(nonce, ciphertext, key)
    tampered_nonce, tampered_cipher = demo.tamper_detection(plaintext)
    try:
        demo.decrypt_payload(tampered_nonce, tampered_cipher, key)
        print("Tamper was not detected.")
    except Exception:
        print("Tamper was detected and rejected.")

    print({
        "shared_secret_matches": shared_secret_a == shared_secret_b,
        "decrypt_success": decrypted == plaintext,
    })


if __name__ == "__main__":
    main()
