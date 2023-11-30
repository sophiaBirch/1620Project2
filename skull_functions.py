'''
    Functionality for the skull jar
    Sophia Birch
    11/29/2023
'''

import time
import random
import numpy as np
import RPi.GPIO as GPIO

# Constants
DB_LIMIT = 75
eye_1 = 12
eye_2 = 16

def init_skull_GPIO():
    # use gpio pin numbering
    GPIO.setmode(GPIO.BCM)

    # set pins as output
    GPIO.setup(eye_1, GPIO.OUT)
    GPIO.setup(eye_2, GPIO.OUT)

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
