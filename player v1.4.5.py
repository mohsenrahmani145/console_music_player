import datetime
import sys
import threading
import time
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pygame import mixer
from tkinter import Tk
from tkinter import filedialog


def player(filename):
    mixer.init()
    mixer.music.load(f"{filename}")
    mixer.music.play()
    while mixer.music.get_busy():
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
            print("___________________________")
            sys.exit()


def main():

    repeat = ""

    while True:
        try:
            print("Please enter a file name: ")
            input_name = str(input())

            if input_name.lower() == "exit":
                sys.exit()
            elif input_name.lower() == "repeat":
                input_name = repeat
            elif input_name.lower() == 'import':
                root = Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(
                    filetypes=[("MP3 - MPEG Layer-3 Audio", ".mp3")])
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

            p1 = threading.Thread(target=timer, args=(length,))
            p1.start()
            player(input_name)
            if input_name != "repeat" and input_name.split('.')[-1].lower() == "mp3":
                repeat = input_name

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
os.system('cls||clear')
print("Wellcome to console music player v1.4.5")
main()
