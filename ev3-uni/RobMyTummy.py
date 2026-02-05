#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep
import time

# --- Hardware Initialisierung ---
drive = MoveTank(OUTPUT_A, OUTPUT_B)
us = UltrasonicSensor(INPUT_2)
ls1 = LightSensor(INPUT_4)  # Rechts
ls2 = LightSensor(INPUT_3)  # Mitte
ls3 = LightSensor(INPUT_1)  # Links
sound = Sound()

# --- Globale Konfiguration ---
active = True
speed = 40
lenken_speed = 30
wenden_speed = 40

# M ist beim Fahren auf der Linie ca. 18 (Schwarz).
middle_val = 21

MAX_BARCODE_GAP_DURATION = 0.8
# Zeit zwischen Streifen ist bis zu 1.2s -> Timeout auf 2.0s erhöhen
BARCODE_TOTAL_TIMEOUT = 2.0
# Erkennung startet ab Wert 28 (21 + 7)
GAP_THRESHOLD = 7

# Barcode Zustand
streifen = 0
in_gap = False
gap_start_time = 0
last_gap_finished_time = 0


def read_vals():
    """Liest Lichtwerte und korrigiert den Hardware-Offset von Sensor Rechts."""
    l = int(ls3.reflected_light_intensity)
    m = int(ls2.reflected_light_intensity)
    # R ist laut Daten ca. 10 heller als L -> Korrektur -10
    r = int(ls1.reflected_light_intensity) - 10
    return l, m, r


def schranke():
    print("LOGIK: Schranke - Warte...")
    drive.off()
    while us.distance_centimeters - 4 < 20:
        sleep(0.1)
    print("Schranke offen.")


def compare_simple(l, m, r, t=5):
    """Simplified navigation logic using light sensors only."""
    if m < l - t and m < r - t:
        return "forward"
    if l < r - t:
        return "left"
    if r < l - t:
        return "right"
    return None


def schieben():
    """Specific behavior for pushing objects."""
    right_till_line()
    while True:
        l, m, r = read_vals()
        interpret(compare_simple(l, m, r))
        d = us.distance_centimeters - 4
        if d < 5:
            while d < 10:
                l, m, r = read_vals()
                d = us.distance_centimeters - 4
                interpret(compare_simple(l, m, r))
            wenden()
            while True:
                l, m, r = read_vals()
                if (abs(r - m) <= 5) or (abs(m - l) <= 5):
                    break
                interpret(compare_simple(l, m, r))
            right_till_line()


def right_till_line():
    """right turn using single-call sensor reading."""
    right()
    sleep(1)
    while True:
        l, m, r = read_vals()
        if not (abs(r - m) <= 5 and abs(m - l) <= 5):
            break
        right()
    return


def left_till_line():
    """left turn using single-call sensor reading."""
    left()
    sleep(1)
    while True:
        l, m, r = read_vals()
        if not (abs(r - m) <= 5 and abs(m - l) <= 5):
            break
        left()
    return


def wenden():
    print("LOGIK: Wand erkannt -> Wenden")
    drive.on_for_rotations(SpeedPercent(20), SpeedPercent(20), 0.2)
    drive.on_for_rotations(SpeedPercent(wenden_speed), SpeedPercent(-wenden_speed), 2.3)


def ziel():
    global active
    print("!!! ZIEL ERREICHT !!!")
    drive.off()
    sound.beep()
    active = False


def forward(s):
    drive.on(SpeedPercent(-s), SpeedPercent(-s))


def right():
    drive.on(SpeedPercent(-lenken_speed), SpeedPercent(5))


def left():
    drive.on(SpeedPercent(5), SpeedPercent(-lenken_speed))


def compare(l, m, r, d, t=10):
    """Präzise Barcode-Logik basierend auf realen Messwerten."""
    global streifen, in_gap, gap_start_time, last_gap_finished_time

    # 1. Hindernis-Erkennung (bleibt gleich, d < 15)
    if d < 15:
        # Erhöhte Toleranz für stabilere Wand-Erkennung (15 statt 5)
        is_flat = abs(l - r) <= 15
        if is_flat:
            avg_outer = (l + r) / 2
            # Laut Daten: Wand ~42, Ziel < 35
            if avg_outer > 38:
                return "wenden"
            else:
                return "ziel"
        else:
            return "schranke"

    # 2. BARCODE-LOGIK (KORRIGIERT)
    now = time.time()
    # Trigger bei m > 28
    is_bright = (m > middle_val + GAP_THRESHOLD)

    if is_bright and not in_gap:
        gap_start_time = now
        in_gap = True
    elif not is_bright and in_gap:
        gap_duration = now - gap_start_time
        in_gap = False

        # Prüfen, ob die Dauer (0.05s bis 0.8s) passt
        if 0.05 < gap_duration < MAX_BARCODE_GAP_DURATION:
            # Falls der letzte Streifen länger als 2s her ist: Neustart bei 1
            if (now - last_gap_finished_time) > BARCODE_TOTAL_TIMEOUT:
                streifen = 1
                print("Barcode: Erster Streifen (Dauer: {:.2f}s)".format(gap_duration))
            else:
                streifen += 1
                print("Barcode: Streifen {} (Dauer: {:.2f}s)".format(streifen, gap_duration))

            last_gap_finished_time = now

    if streifen >= 2:
        streifen = 0
        print("AKTION: SCHIEBEN")
        return "schieben"

    # 3. Linien-Navigation
    if l < r - t:
        return "left"
    if r < l - t:
        return "right"

    return "forward"


def interpret(action):
    if action == "forward":
        forward(speed)
    elif action == "left":
        left()
    elif action == "right":
        right()
    elif action == "wenden":
        wenden()
    elif action == "schranke":
        schranke()
    elif action == "ziel":
        ziel()
    elif action == "schieben":
        print("AKTION: Schieben gestartet")
        schieben()


print("Start... Basiswert:", middle_val)

while active:
    l_val, m_val, r_val = read_vals()
    dist = us.distance_centimeters - 4

    entscheidung = compare(l_val, m_val, r_val, dist)
    interpret(entscheidung)

    sleep(0.01)
