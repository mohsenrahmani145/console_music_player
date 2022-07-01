import datetime
import sys
import threading
import time
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from pygame import mixer


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
        if zerotime > length:
            sys.exit()

def main():

    input_name = str(input("Please enter a file name: "))
    
    
    try:
        length = int(MP3(f"{input_name}").info.length) 
        info = int(MP3(input_name).info.bitrate)
        p1 = threading.Thread(target=timer, args=(length,))
        
        print("Name: " + input_name.split("\\")[-1])
        try:
            print("Artist: " + ID3(input_name)['TPE1'].text[0]) #Artist
            print("Track: " + ID3(input_name)['TIT2'].text[0]) #Track   
        
        except Exception:
            pass

        print(f"Bitrate: {int(info/1000)} kbps")
        print("Length: " +
            str(datetime.timedelta(seconds=length))) #length
        p1.start()
        player(input_name)

    except Exception:
        print("File not found")
        main()

        
os.system('cls||clear')
print("Wellcome to console music player v1.0.0")
main()
