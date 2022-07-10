import datetime
import sys
import threading
import time
import os
import keyboard
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pygame import mixer
from tkinter import Tk
from tkinter import filedialog


def key_event(hot_key):
    try:
        keyboard.record(hot_key)
        key_stop.set()
    except Exception:
        pass


def player(filename):
    key_stop.clear()
    mixer.init()
    mixer.music.load(f"{filename}")
    mixer.music.play()
    while mixer.music.get_busy():
        if key_stop.is_set():
            mixer.music.stop()
            print('Audio stopped playing')
        time.sleep(1)


def timer(length):
    zerotime = 0
    length = length

    while True:
        result = str(datetime.timedelta(seconds=zerotime))
        print("Time: " + result, end="")
        print("\r", end="")
        time.sleep(1)
        zerotime += 1
        if stop_thread.is_set():
            break
        if zerotime > length:
            sys.exit()


def main():

    repeat = ""

    while True:
        try:
            print("Please enter a file name: ")
            input_name = str(input())
            if input_name.find("\"") == 0:
                input_name = input_name.split("\"")[1]
            if input_name.lower() == "exit":
                sys.exit()
            if input_name.lower() == "repeat":
                input_name = repeat
            if input_name.lower() == 'import':
                root = Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(filetypes=[(
                    "MP3 - MPEG Layer-3 Audio", "*.mp3")], title="Select A File", parent=root)
                input_name = file_path.replace('/', '\\')

            length = int(MP3(f"{input_name}").info.length)
            info = int(MP3(input_name).info.bitrate)
            print("Name: " + input_name.split("\\")[-1])
            try:
                print("Artist: " + ID3(input_name)['TPE1'].text[0])  # Artist
                print("Track: " + ID3(input_name)['TIT2'].text[0])  # Track
            except Exception:
                pass
            print(f"Bitrate: {int(info/1000)} kbps")
            print("Length: " + str(datetime.timedelta(seconds=length)))  # length
            stop_thread.clear()
            time_elapsed = threading.Thread(target=timer, args=(length,))
            time_elapsed.start()
            stop_event = threading.Thread(target=key_event,args=(("ctrl","s"),))
            stop_event.daemon = True
            stop_event.start()

            player(input_name)
            if input_name != "repeat" and input_name.split('.')[-1].lower() == "mp3":
                repeat = input_name
            print("___________________________")
            stop_thread.set()

        except Exception:
            print("File not found")
        except KeyboardInterrupt:
            mixer.init()
            mixer.music.stop()
            stop_thread.set()
            os.system('cls||clear')
            print("Goodbye! come back soon :)")
            time.sleep(3)
            sys.exit()


stop_thread = threading.Event()
key_stop = threading.Event()
os.system('cls||clear')
print("Wellcome to console music player v1.4.5")
main()
