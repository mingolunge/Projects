#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep
from time import time
import math

# arm = LargeMotor(OUTPUT_C)              # arm
drive = MoveTank(OUTPUT_A, OUTPUT_B)    # Motorsteuerung
us = UltrasonicSensor(INPUT_2)
ls1 = LightSensor(INPUT_1)              # linker Lichtsensor
ls2 = LightSensor(INPUT_3)              # mittlerer Lichtsensor
ls3 = LightSensor(INPUT_4)              # rechter Lichtsensor
sound = Sound()
last_action = ""                        # letzte Fahraktion
active = True
speed = 80
lenken_speed = 50
wenden_speed = 40
middle_val = ((ls1.reflected_light_intensity + ls3.reflected_light_intensity) / 2 + ls2.reflected_light_intensity) / 2  # Initialisierung von middle value weil wir davor 40 hatten
# noch in streifenerkennung machen, dass er sich richtung merkt
# Initialize
streifen = 0
in_gap = False 
last_gap_time = 0
TIMEOUT_LIMIT = 1.5 # Adjust based on robot speed

def read_vals():
    l = ls3.reflected_light_intensity
    r = ls1.reflected_light_intensity / 1.3
    m = ls2.reflected_light_intensity * 1.1
    d = us.distance_centimeters - 4
    return l, m, r, d

def compare(l, m, r, d, t=5):
    global streifen, in_gap, last_gap_time

    # --- 1. Obstacle Check (Highest Priority) ---
    if d < 10:
        return "schranke"
    
    avg = (l + m + r) / 3
    if math.isclose(l, m, abs_tol=5) and math.isclose(m, r, abs_tol=5):
        if d < 20:
            if avg >= middle_val - t:
                return "wenden"
            else: # If it's dark and uniform
                return "ziel"

        current_time = time()
        wsw = r > m and l > m

        if streifen > 0 and (current_time - last_gap_time) > TIMEOUT_LIMIT:
            streifen = 0
            print("resetting timer" , current_time - last_gap_time)

        if not wsw and d > 15:
            streifen += 1
            in_gap = True
            last_gap_time = current_time
            print("streifen: ", streifen, current_time - last_gap_time)
        else:
            in_gap = False

        if streifen == 3:
            streifen = 0 
            return "schieben"

    if l < r - t:
        return "left"
    if r < l - t:
        return "right"

    return "forward"

while True:
    l, m, r, d = read_vals()
    print("d: ", d)
    print(l, m, r)
    print("same color:", math.isclose(l, m, abs_tol=5) and math.isclose(m, r, abs_tol=5))
    print(compare(l, m, r, d))
    sleep(.5)
    print("\n \n")
    
