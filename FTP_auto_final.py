# -*- coding: utf-8 -*-
import os
import time
import threading
import getpass
from ftplib import FTP
from tqdm import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FTP server remote path & OS local path
Rpath = ""
Lpath = r"C:\Users\PSPICE\Desktop\fileSava"

# Variables FTP UID, PWD
username = ""
password = ""

# Class of Monitoring
class Watcher:
    # Set Monitoring Directory
    DIRECTORY_TO_WATCH = Lpath

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print("###### Start Monitoring ######")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt: # Ctrl + C를 누를 경우 프로세스 종료 (인터럽트)
            self.observer.stop()

        self.observer.join()

# Class of Event Handle
class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)

            # Delay some seconds in order to safety file open
            if os.path.getsize(event.src_path) >= 1073741824:
                time.sleep(10)
            else:
                time.sleep(5)

            # Extract file extension
            ext = os.path.splitext(event.src_path)[-1]

            # If file extension is .mp4, perform file upload.
            if ext == '.mp4':
                filename = event.src_path.split('\\')[-1]
                dirname = event.src_path.split('\\')[-2]
                t = threading.Thread(target=ftp_upload(filename, dirname, event.src_path))
                t.start()
            else:
                pass

        else:
            return None

# Function of ftp upload
def ftp_upload(filename, dirname, eventpath):

    # Login to ftp server.
    ftp = FTP("223.194.33.57")
    ftp.login(username, password)
    #print("Connection established.")

    # File open
    file = open(eventpath, 'rb')
    filesize = os.path.getsize(eventpath)
    # Set upload path - Server path
    ftp.cwd("ABO/")

    # Perform upload and Show user for progress bar
    with tqdm(unit='blocks', unit_scale=True, leave=False, miniters=1, desc="Uploading...",
              total=filesize) as tqdm_instance:
        ftp.storbinary('STOR ' + filename, file, 20480, callback=lambda sent: tqdm_instance.update(len(sent)))
    print("\nFile transfer successful.\n")

    # Close ftp server.
    ftp.quit()
    # Close file open().
    file.close()

# Function of FTP Account Check
def CheckAccount():
    try:
        ftp = FTP("223.194.33.57")
        ftp.login(username, password)
        ftp.close()
        return True
    except Exception as e:
        print(e)
        ftp.close()
        print("FTP close!")
        return False

if __name__ == '__main__':

    # Check FTP Account Info
    while True:
        print("###### Enter the ftp ID and Password ######")
        username = input("ID: ")
        password = getpass.getpass(prompt="Password: ")

        if CheckAccount():
            print("Verified!\n")
            break
        else:
            print("Please check FTP ID or Password.\n")
            continue

    w = Watcher()
    w.run()
