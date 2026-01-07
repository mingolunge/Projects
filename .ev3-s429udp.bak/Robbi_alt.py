#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep


def forward(speed: int):  # beide Motoren vorwärts fahren
    drive.on(SpeedPercent(-speed), SpeedPercent(-speed))


def right():  # Rechtskurve
    drive.on(SpeedPercent(0), SpeedPercent(-wenden_speed))


def left():  # Linkskurve
    global wenden_speed
    drive.on(SpeedPercent(-wenden_speed), SpeedPercent(0))


def wenden():  # Wenden
    drive.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 1) # Rückwärts
    drive.on_for_rotations(SpeedPercent(-50), SpeedPercent(50), 1.6)  # 180° drehen


def on_line(rl):  # prüft, ob Sensor einen schwarzen Streifen sieht
    return rl < threshold


def compare(l, m, r, t=5):
    if m < (l + r) / 2 + t:
        return "forward"
    if l < r + t:  # wenn links auf linie und rechts nicht dann unter if clause
        if m < r + t:
            return "left"
        elif m >= r - t:
            return "left"
    if r < l + t:  # wenn links auf linie und rechts nicht dann unter if clause
        if m < l + t:
            return "left"
        elif m >= l - t:
            return "left"



def ziel():  # Ziel- Melodie abspielen
    i=0
    global active
    drive.off() # anhalten
    # Hier noch einbauen dass er winkt und sich dreht
    sound.play_file("sound.wav", volume=100)#, play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
    active = False  # Stoppt die  main while loop


def obstacle():
    drive.off() # bisschen nach vorne
    while True:
        distance = us.distance_centimeters
        if distance >= 10:  # weg frei
            break
        sleep(.1)


def schieben():  # Block Schieben
    forward(100)
    while us.distance_centimeters > 5:  # fährt mit forward(100) während die distanz größer als 3cm ist und geht zur nächsten schleife
        sleep(.01) 

    while us.distance_centimeters <= 10:  # solange die Distanz die der Sensor misst kleiner als 5 misst fährt er nach vorne, langsam
        forward(10)
        sleep(.01)
    wenden()  # Wenn die while loop dur einen abstandswert höher als 5cm abbricht, wendet der ryoboter direkt


def streifenzähler():
    global streifen
    forward(20)
    s = 0
    while s < 40:
        if not on_line(l) and not on_line(m) and not on_line(r):
            streifen += 1
            s += 1
            sleep(.1)


def right_90():  # 90° Rechtsdrehung für barcode
    drive.on_for_rotations(SpeedPercent(60), SpeedPercent(-60), 0.8)  # 90° Drehung


drive = MoveTank(OUTPUT_A, OUTPUT_B)    # Motorsteuerung
ls1 = LightSensor(INPUT_1)              # linker Lichtsensor
ls2 = LightSensor(INPUT_3)              # mittlerer Lichtsensor
ls3 = LightSensor(INPUT_4)              # rechter Lichtsensor
us = UltrasonicSensor(INPUT_2)          # Ultraschallsensor
sound = Sound()                         # Soundmodul

threshold = calibrate_ls()              # Anfangsschwelle setzen
last_action = None                      # letzte Fahraktion
active = True                           # Condition für die main-loop
streifen = 0                            # Zähler für weiße Streifen

speed = 70                            # Geschwindigkeitsvariable für Geradeaus
wenden_speed = 60                       # Geschwindigkeitsvariable für kurven

# sound.play_file('runnin.wav', play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

while active:
    # Sensorwerte lesen
    l = ls1.reflected_light_intensity
    m = ls2.reflected_light_intensity
    r = ls3.reflected_light_intensity
    us_val = us.distance_centimeters

    # Hindernis
    if us_val <= 10:
        if not on_line(l) and not on_line(m) and not on_line(r):
            wenden()
        else:
            obstacle()

    # Ziel erreicht (alle Sensoren auf Linie)
    elif on_line(l) and on_line(m) and on_line(r) and us_val <= 25:
        ziel()

    # Linkskurve
    elif on_line(m) and on_line(l):
        left()
        last_action = "left"

    # Rechtskurve
    elif on_line(m) and on_line(r):
        right()
        last_action = "right"

    # Geradeaus
    elif on_line(m):
        forward(speed)
        last_action = "forward"

    # Nur links auf Linie -> Links fahren
    elif on_line(l):
        left()
        last_action = "left"

    # Nur rechts auf Linie -> Rechts fahren
    elif on_line(r):
        right()
        last_action = "right"

    # Keine Linie erkannt -> letzte Aktion wiederholen
    elif not on_line(l) and not on_line(m) and not on_line(r):
        streifen += 1  # Streifenzähler

        if last_action == "forward":
            forward(speed)
        elif last_action == "right":
            right()
        elif last_action == "left":
            left()
