import speech_recognition as sr
from termcolor import colored
import simpleaudio as sa
import sounddevice
import subprocess
import webbrowser
import time
import sys
import re


start_sound = sa.WaveObject.from_wave_file("/home/milo/Documents/Python/Voicebot/sounds/start.wav")
stop_sound = sa.WaveObject.from_wave_file("/home/milo/Documents/Python/Voicebot/sounds/stop.wav")
error_sound = sa.WaveObject.from_wave_file("/home/milo/Documents/Python/Voicebot/sounds/error.wav")
alarm_sound = sa.WaveObject.from_wave_file("/home/milo/Documents/Python/Voicebot/sounds/alarm.wav")

recognizer = sr.Recognizer()
mic = sr.Microphone()


def start_vol_down():
    start_vol_down = 25
    while start_vol_down >= 0:
        subprocess.run("pactl set-sink-volume 0 -1%", shell = True)
        start_vol_down -= 1
        time.sleep(0.001)

def end_vol_up():
    end_vol_up = 25
    while end_vol_up >= 0:
        subprocess.run("pactl set-sink-volume 0 +1%", shell = True)
        end_vol_up -= 1
        time.sleep(0.001)

def extract_number_from_script(script):
    # Use regular expressions to extract the number from the script
    number_match = re.search(r'\d+', script)
    if number_match:
        number = int(number_match.group())
        return number
    else:
        return None

def set_timer(demand):
    time_timer = extract_number_from_script(demand)
    print(f"Timer set for {time_timer} minutes...")
    time.sleep(time_timer * 60)
    print("timer ran out")
    play_object = alarm_sound.play()
    play_object.wait_done()

def calibrate_mic():
    with mic as source:
        print(colored("Calibrating...", "cyan"))
        recognizer.adjust_for_ambient_noise(mic, duration=3)
        print(colored("Finished calibrating!", "cyan"))

def recalibrate_mic():
    print(colored("Calibrating...", "cyan"))
    recognizer.adjust_for_ambient_noise(mic, duration=3)
    print(colored("Finished calibrating!", "cyan"))

def volume_up(demand):
    if "three times" in demand:
        vol_3x = 0
        while vol_3x < 3:
            subprocess.run("pactl set-sink-volume 0 +5%", shell = True)
            vol_3x += 1
            time.sleep(0.2)
    else:
        subprocess.run("pactl set-sink-volume 0 +5%", shell = True)


def volume_down(demand):
    if "three times" in demand:
        vol_3x = 0
        while vol_3x < 3:
            subprocess.run("pactl set-sink-volume 0 -5%", shell = True)
            vol_3x += 1
            time.sleep(0.2)
    else:
        subprocess.run("pactl set-sink-volume 0 -5%", shell = True)

def web_search(demand):
    char_to_replace = {'search for ': '', " online" : "", " ": "+"}
    for key, value in char_to_replace.items():
        demand = demand.replace(key, value)
    webbrowser.open("https://www.google.com/search?q=" + demand)


def youtube_search(demand):
    char_to_replace = {'search ': '', ' on ': '', 'youtube': '', " ": "+"}
    for key, value in char_to_replace.items():
        demand = demand.replace(key, value)
    webbrowser.open("https://www.youtube.com/results?search_query=" + demand)
