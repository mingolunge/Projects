from piper import PiperVoice
import sounddevice as sd
import numpy as np
import subprocess
from time import sleep
import ollama
import speech_recognition as sr
import webbrowser
from random import randint

recognizer = sr.Recognizer()
mic = sr.Microphone()
model = "v_model/en_US-bmo_voice.onnx"
voice = PiperVoice.load(model)
stream = sd.OutputStream(
    samplerate=voice.config.sample_rate, 
    channels=1, 
    dtype='int16'
)
stream.start()

messages = [{'role': 'user', 'content': "Dont use '?' ever! Youre an AI but your name is BEEMO and my name is Milo. keep answers short like a regular conversation. Youre a real person, not a chatbot."}]
model_name = 'smollm2:latest'
ollama.pull(model_name)

def ask_question(prompt):
    messages.append({'role': 'user', 'content': prompt})
    
    response = ollama.chat(model=model_name, messages=messages)
    
    bot_message = response['message']['content']
    messages.append({'role': 'assistant', 'content': bot_message})
    
    return bot_message

def say(text:str):
    for chunk in voice.synthesize(text):
        stream.write(chunk.audio_int16_array)


def listen(limit: int):
    audio = recognizer.listen(source, phrase_time_limit = limit)
    return recognizer.recognize_vosk(audio).lower()

def web_search(promt):
    char_to_replace = {'search for ': '', "search up " : "", " ": "+"}
    for key, value in char_to_replace.items():
        promt = promt.replace(key, value)
    webbrowser.open("https://www.google.com/search?q=" + promt)


with mic as source:
    recognizer.adjust_for_ambient_noise(mic, duration=3)

print("model initialized")
say("All Booted up")

affirmative = ["on it", "will do", "yes"]
attention = ["yeah", "yes", "yup", "huh"]
wakewords = ["alexa","bemo", "beemo", "be more", "emo", "demo"]
while True:
    try:
        with mic as source:
            said = listen(20)
            print(said)
            if any(word in said for word in wakewords):
                say(attention[randint(0, len(attention))])
                promt = listen(5)
                print(promt)
                say(affirmative[randint(0, len(affirmative))])
                if "skip" in promt and "song" in promt: #skip song
                    subprocess.call(("playerctl", "next"))
                elif "pause" in promt or "play" in promt: #pause/play song
                    subprocess.call(("playerctl", "play-pause"))
                elif "goodbye" in promt:
                    quit()
                elif "search for" in promt or "search up" in promt:
                    web_search(promt)
                else:
                    say(ask_question(promt))
                
    except:
        pass

stream.stop()
stream.close()
