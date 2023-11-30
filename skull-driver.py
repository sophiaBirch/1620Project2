'''
    Script to drive functionality of the skull jar

    by Sophia Birch
    11/26/2023
'''
import time
import pygame
import pyaudio
from os import listdir
from os.path import isfile, join
from threading import Timer

from skull_functions import *

def main():
    # setup

    # initalize timestamp to epoch, used to only play one voice line at once
    DONT_GO_UNTIL = 0

    # init pygame mixer
    pygame.mixer.init()

    init_skull_GPIO()

    # sound clips. will eventually be an array of skeletor voicelines
    audio_dir = "./audio/"
    soundfiles = [f for f in listdir(audio_dir) if isfile(join(audio_dir, f))] # https://stackoverflow.com/a/3207973
    sound_array = [pygame.mixer.Sound(audio_dir + file) for file in soundfiles if file.endswith(".wav")]

    # pyaudio constants
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    py_audio = pyaudio.PyAudio()
    STREAM = py_audio.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

    while(True):
        data = STREAM.read(CHUNK)
        received = detect_vibes(data)

        if received and (time.time() > DONT_GO_UNTIL):
            print("By the power of GReYsKuLl!!!!")

            audio = randomize_audio(sound_array)

            audio.play()

            r = Timer(0.1, activate_LED, (audio.get_length(),))
            # activate_LED(audio.get_length())
            r.start()

            # prevents activation of audio until current audio has finished playing
            DONT_GO_UNTIL = time.time() + audio.get_length() + 0.5
            print("I won't go again until", DONT_GO_UNTIL, "and right now its", time.time())

            print("finishing audio")

if __name__ == "__main__":
    main()
