from cryptography.fernet import Fernet
import os

LOG_FOLDER = "logs"
KEY_FILE = "secret.key"
ENCRYPTED_FILE = os.path.join(LOG_FOLDER, "keylog_encrypted.txt")
DECRYPTED_FILE = os.path.join(LOG_FOLDER, "decrypted_log.txt")

print(f"[~] Looking for key in: {KEY_FILE}")
print(f"[~] Looking for encrypted log at: {ENCRYPTED_FILE}")
print(f"[~] Will write decrypted log to: {DECRYPTED_FILE}")

# Load the key
if not os.path.exists(KEY_FILE):
    print("[!] Encryption key not found.")
    exit()

with open(KEY_FILE, "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

# Decrypt the log
try:
    if not os.path.exists(ENCRYPTED_FILE):
        print("[!] Encrypted file not found.")
        exit()

    with open(ENCRYPTED_FILE, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
        print(f"[~] Encrypted data size: {len(encrypted_data)} bytes")

    decrypted_data = fernet.decrypt(encrypted_data)

    with open(DECRYPTED_FILE, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
        print("[*] Decrypted data written successfully.")

    print(f"[✓] Decryption successful. File saved as: {DECRYPTED_FILE}")

except Exception as e:
    print(f"[!] Error during decryption: {e}")
