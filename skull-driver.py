'''
    Script to drive functionality of the skull jar

    by Sophia Birch
    11/26/2023
'''
from skull_functions import *
def main():
    while(True):
        data = STREAM.read(CHUNK)
        received = detect_vibes(data)

        if received and (time.time() > DONT_GO_UNTIL):
            print("By the power of GReYsKuLl!!!!")
            play_audio(randomize_audio(sound_array))
            print("finishing audio")

if __name__ == "__main__":
    main()
