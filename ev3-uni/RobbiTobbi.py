#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep
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
speed = 30
lenken_speed = 30
wenden_speed = 30
middle_val = ((ls1.reflected_light_intensity + ls3.reflected_light_intensity) / 2 + ls2.reflected_light_intensity) / 2  # Initialisierung von middle value weil wir davor 40 hatten
# noch in streifenerkennung machen, dass er sich richtung merkt


def read_vals():
    l = ls3.reflected_light_intensity
    r = ls1.reflected_light_intensity / 1.2
    m = ls2.reflected_light_intensity * 1.1
    d = us.distance_centimeters - 4
    return l, m, r, d


def schranke(d=read_vals()[3]):
    drive.off()  # anhalten
    while d < 10:  # Wartet bis tor auf
        sleep(.1)
    return  # zurück in die main loop


def compare_simple(l, m, r, d, t=5):
    avg = (l + m + r) / 3
    if m < l - t and m < r - t:
        return "forward"
    if l < r - t:
        return "left"
    if r < l - t:
        return "right"
    return None


def schieben(d=read_vals()[3]):
    right_till_line()
    while True:
        interpret(compare_simple(*read_vals()))
        d = read_vals()[3]
        if d < 5:
            while d < 10:
                d = read_vals()[3]
                forward(10)
            wenden()
            vals = read_vals()
            while not math.isclose(vals[2], vals[1], abs_tol=5) and not math.isclose(vals[1], vals[0], abs_tol=5):
                forward(10)
                vals = read_vals()
            right_till_line()


def wenden():  # Wenden
    drive.on_for_rotations(SpeedPercent(wenden_speed), SpeedPercent(wenden_speed), 1)  # Rückwärts
    drive.on(SpeedPercent(wenden_speed), SpeedPercent(-wenden_speed))  # drehen
    sleep(2)
    while math.isclose(read_vals()[2], read_vals()[1], abs_tol=5) and math.isclose(read_vals()[1], read_vals()[0], abs_tol=5):  # solange www/sss: linie suchen
        drive.on(SpeedPercent(wenden_speed), SpeedPercent(-wenden_speed))  # drehen
    return


def ziel():  # Ziel- Melodie abspielen
    global active
    drive.off()  # anhalten
    # arm.on_for_rotations(SpeedPercent(10), SpeedPercent(10), .25)

    # Hier noch einbauen dass er winkt und sich dreht
    # sound.play_file("sound.wav", volume=100)#, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
    active = False  # Stoppt die  main while loop


def forward(speed: int):  # beide Motoren vorwärts fahren
    drive.on(SpeedPercent(-speed), SpeedPercent(-speed))


def right():  # Rechtskurve
    drive.on(SpeedPercent(-lenken_speed), SpeedPercent(0))


def left():  # Linkskurve
    drive.on(SpeedPercent(0), SpeedPercent(-lenken_speed))


def right_till_line():  # Rechtskurve
    right()
    sleep(1)
    while math.isclose(read_vals()[2], read_vals()[1], abs_tol=5) and math.isclose(read_vals()[1], read_vals()[0], abs_tol=5):  # solange rechts fahren bis linie erkannt
        right()  # drehen
    return


def left_till_line():  # Linkskurve
    left()
    sleep(1)
    while math.isclose(read_vals()[2], read_vals()[1], abs_tol=5) and math.isclose(read_vals()[1], read_vals()[0], abs_tol=5):  # solange linbks fahren bis linie erkannt
        left()  # links
    return


def compare(l, m, r, d, t=5):
    avg = (l + m + r) / 3
    if math.isclose(l, m, abs_tol=5) and math.isclose(m, r, abs_tol=5):
        if d < 20:
            if avg >= middle_val - t:
                return "wenden"
            if avg < middle_val:
                return "ziel"
            else:
                pass
    if m < l - t and m < r - t:
        if d < 5:
            return "schranke"
        

        
        return "forward"
    if l < r - t:
        return "left"
    if r < l - t:
        return "right"
    return None


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
        drive.off()
        sleep(.5)
        ziel()
    elif x == "schranke":
        schranke()
    elif x == "wenden":
        wenden()
        last_action = "forward"
    else:
        if last_action == "right":
            right()
        elif last_action == "left":
            left()
        if last_action == "forward":
            forward(speed)


while True:
    interpret(compare(*read_vals()))
