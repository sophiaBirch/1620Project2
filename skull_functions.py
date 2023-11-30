'''
    Functionality for the skull jar
    Sophia Birch
    11/29/2023
'''
import time
import RPi.GPIO as GPIO
import pygame
import random
import pyaudio
import numpy as np

from threading import Timer

from os import listdir
from os.path import isfile, join

# initalize timestamp to epoch, used to only play one voice line at once
DONT_GO_UNTIL = 0

# pin defs
eye_1 = 12
eye_2 = 16

# decibel lower limit for activation
DB_LIMIT = 75

# use gpio pin numbering
GPIO.setmode(GPIO.BCM)

# set pins as output
GPIO.setup(eye_1, GPIO.OUT)
GPIO.setup(eye_2, GPIO.OUT)

# init pygame mixer
pygame.mixer.init()

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

def activate_LED(duration) -> None:
    '''
        While audio is playing (duration), keep the eyes lit up.
    '''

    print("Eyes will be lit for:", duration, "seconds")

    GPIO.output(eye_1, GPIO.HIGH)
    GPIO.output(eye_2, GPIO.HIGH)

    time.sleep(duration)

    GPIO.output(eye_1, GPIO.LOW)
    GPIO.output(eye_2, GPIO.LOW)
    return


def play_audio(audio) -> None:
    '''
        Plays audio clip and activates the eyes.
    '''
    audio.play()

    r = Timer(0.1, activate_LED, (audio.get_length(),))
    # activate_LED(audio.get_length())
    r.start()

    # prevents activation of audio until current audio has finished playing
    global DONT_GO_UNTIL
    DONT_GO_UNTIL = time.time() + audio.get_length() + 0.5
    print("I won't go again until", DONT_GO_UNTIL, "and right now its", time.time())

    return


def randomize_audio(array):
    '''
        Select at random a clip from the array of voicelines

        :param: array of pygame sounds
        :return: a single pygame sound from the array (element)
    '''
    # select a random number
    j = random.randrange(0, len(array))

    #return the element of the array at that number
    element = array[j]
    return element

def detect_vibes(data) -> bool:
    '''
        Detects vibrations within a decibel range from the contact mic.

        :param: data: a chunk of a waveform of size CHUNK
        :return: true (data contains audio within decibel level), false (data does not contain audio within decibel level
    '''
    audio_data = np.frombuffer(data, dtype = np.int16)
    db = 20 * np.log10(np.abs(np.max(audio_data)))

    if db > DB_LIMIT:
        print(db)
    
    return db > DB_LIMIT

