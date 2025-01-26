import datetime
import os

username = os.getenv('username')
log_path = f"C:\\Users\\{username}\\Documents\\"

def write_log(message, type='info'):
    with open(log_path+'main_log.txt', 'a+') as log_file:
        log_file.write(f"[{type.upper()}] - {message} - {datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')}\n")
