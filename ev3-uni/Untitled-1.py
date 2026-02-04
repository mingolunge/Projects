#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep
import time

# Hardware initialization
drive = MoveTank(OUTPUT_A, OUTPUT_B)
us = UltrasonicSensor(INPUT_2)
ls1 = LightSensor(INPUT_4)
ls2 = LightSensor(INPUT_3)
ls3 = LightSensor(INPUT_1)
sound = Sound()

# Global configuration and state
last_action = ""
active = True
speed = 80
lenken_speed = 50
wenden_speed = 50

# Initial calibration
middle_val = ((ls1.reflected_light_intensity + ls3.reflected_light_intensity) / 2 + ls2.reflected_light_intensity) / 2

# Barcode state tracking
streifen = 0
in_gap = False
gap_start_time = 0
last_gap_finished_time = 0

# Tuning Constants
MAX_BARCODE_GAP_DURATION = 0.15
BARCODE_TOTAL_TIMEOUT = 1.0
GAP_THRESHOLD = 15


def read_vals():
    """Fetches current light levels with hardware scaling."""
    l = ls3.reflected_light_intensity
    r = ls1.reflected_light_intensity / 1.2
    m = ls2.reflected_light_intensity * 1.1
    return l, m, r


def schranke():
    """Stops motors and waits until an obstacle is cleared."""
    drive.off()
    d = us.distance_centimeters - 4
    while d < 15:
        d = us.distance_centimeters - 4
        sleep(.1)
    return


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
                d = us.distance_centimeters - 4
                forward(10)
            wenden()
            while True:
                l, m, r = read_vals()
                if (abs(r - m) <= 5) or (abs(m - l) <= 5):
                    break
                forward(10)
            right_till_line()


def wenden():
    """Performs a 180-degree turn sequence."""
    drive.on_for_rotations(SpeedPercent(wenden_speed), SpeedPercent(wenden_speed), 1)
    drive.on_for_rotations(SpeedPercent(wenden_speed), SpeedPercent(-wenden_speed), 2)


def ziel():
    """Triggers end-of-run and halts loop."""
    global active
    drive.off()
    active = False


def forward(speed: int):
    drive.on(SpeedPercent(-speed), SpeedPercent(-speed))


def right():
    drive.on(SpeedPercent(-lenken_speed), SpeedPercent(0))


def left():
    drive.on(SpeedPercent(0), SpeedPercent(-lenken_speed))


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


def compare(l, m, r, d, t=5):
    """Main decision engine for navigation and barcode detection."""
    global streifen, in_gap, gap_start_time, last_gap_finished_time

    if d < 10:
        return "schranke"

    now = time.time()
    is_bright = (m > middle_val + GAP_THRESHOLD)

    if is_bright and not in_gap:
        gap_start_time = now
        in_gap = True
    elif not is_bright and in_gap:
        gap_duration = now - gap_start_time
        in_gap = False

        if gap_duration < MAX_BARCODE_GAP_DURATION:
            if (now - last_gap_finished_time) > BARCODE_TOTAL_TIMEOUT:
                streifen = 1
            else:
                streifen += 1
                print("+1 streifen", streifen)
            last_gap_finished_time = now
        else:
            streifen = 0

    if streifen >= 3:
        streifen = 0
        return "schieben"

    avg = (l + m + r) / 3
    if abs(l - m) <= 5 and abs(m - r) <= 5:
        if d < 20:
            if avg >= middle_val - t:
                return "wenden"
            else:
                return "ziel"

    if l < r - t:
        return "left"
    if r < l - t:
        return "right"

    return "forward"


def interpret(x: str):
    """Translates logic strings into motor commands."""
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
    elif x == "barcode_action":
        # Placeholder for what happens when 3 fast gaps are seen
        drive.off()
        sound.beep()
        last_action = "forward"
    elif x == "schieben":
        schieben()
    else:
        if last_action == "right":
            right()
        elif last_action == "left":
            left()
        elif last_action == "forward":
            forward(speed)


while True:
    l, m, r = read_vals()
    print("L: ", l, "  M: ", m, "  R:", r)
    sleep(.5)