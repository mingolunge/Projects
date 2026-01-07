#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep


drive = MoveTank(OUTPUT_A, OUTPUT_B)    # Motorsteuerung
ls1 = LightSensor(INPUT_1)              # linker Lichtsensor
ls2 = LightSensor(INPUT_3)              # mittlerer Lichtsensor
ls3 = LightSensor(INPUT_4)
us = UltrasonicSensor(INPUT_2)          # rechter Lichtsensor
last_action = None                      # letzte Fahraktion
active = True
sound = Sound()


def wenden():  # Wenden
    drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 1) # Rückwärts
    drive.on_for_rotations(SpeedPercent(-50), SpeedPercent(50), 1.6)  # 180° drehen


def ziel():  # Ziel- Melodie abspielen
    global active
    drive.off() # anhalten
    # Hier noch einbauen dass er winkt und sich dreht
    # sound.play_file("sound.wav", volume=100)#, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
    active = False  # Stoppt die  main while loop


def forward(speed: int):  # beide Motoren vorwärts fahren
    drive.on(SpeedPercent(-speed), SpeedPercent(-speed))


def right():  # Rechtskurve
    drive.on(SpeedPercent(-wenden_speed), SpeedPercent(0))


def left():  # Linkskurve
    drive.on(SpeedPercent(0), SpeedPercent(-wenden_speed))


# sound.play_file('runnin.wav', play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
def compare(l, m, r, d, t=5):
    if m < l - t and m < r - t:
        return "forward"

    if l < r - t:
        return "left"

    if r < l - t:
        return "right"

    if (l + m + r) / 3 < avg and d < 20:
        return "ziel"

    if d < 8:
        return "wenden"

    if l > avg and m > avg and r > avg:
        return "panic"

    return None


last_action = ""

def interpret(x: str):
    global last_action
    if x == "forward":
        forward(speed)
        last_action = "forward"
    elif x == "right":
        right()
        last_action = "right"
    elif x == "left":
        left()
        last_action = "left"
    elif x == "ziel":
        ziel()
    elif x == "wenden":
        wenden()
    elif x == "panic":
        if last_action == "right":
            right()
        elif last_action == "left":
            left()
        if last_action == "forward":
            forward(speed)


avg = (ls1.reflected_light_intensity / 1.2 + ls2.reflected_light_intensity * 1.1 + ls3.reflected_light_intensity) / 3
speed = 70
wenden_speed = 60


while True:
    # Sensorwerte lesen
    r = ls1.reflected_light_intensity / 1.2
    m = ls2.reflected_light_intensity * 1.1
    l = ls3.reflected_light_intensity
    d = us.distance_centimeters - 4
    print("\n\n")
    print("L: ", l)
    print("M: ", m)
    print("R: ", r)
    print("U: ", d)
    sleep(.5)