#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, SpeedPercent, MoveTank, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import LightSensor, UltrasonicSensor
from ev3dev2.sound import Sound
from time import sleep
import time

# Hardware initialization
arm = LargeMotor(OUTPUT_C)
drive = MoveTank(OUTPUT_A, OUTPUT_B)
us = UltrasonicSensor(INPUT_2)
ls1 = LightSensor(INPUT_4)
ls2 = LightSensor(INPUT_3)
ls3 = LightSensor(INPUT_1)
sound = Sound()

# Global configuration and state
last_action = ""
active = True
speed = 100
lenken_speed = 75
wenden_speed = 40

# Initial calibration
middle_val = int((ls1.reflected_light_intensity + ls3.reflected_light_intensity + ls2.reflected_light_intensity * 2) / 4)


def read_vals():
    """Fetches current light levels with hardware scaling."""
    l = int(ls3.reflected_light_intensity)
    m = int(ls2.reflected_light_intensity)
    r = int(ls1.reflected_light_intensity) - 10
    return l, m, r


def schranke():
    """Stops motors and waits until an obstacle is cleared."""
    drive.off()
    d = us.distance_centimeters - 4
    while d < 20:
        d = us.distance_centimeters - 4
        sleep(.1)
    return


def compare_simple(l, m, r, t=5):
    """Simplified navigation logic using light sensors only."""
    if l < r - t:
        return "left"
    if r < l - t:
        return "right"
    return "forward"


def schieben():
    """Specific behavior for pushing objects."""
    print("schieben funct")
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


def wenden():
    """Performs a 180-degree turn sequence."""
    l, m, r = read_vals()
    # drive.on_for_rotations(SpeedPercent(wenden_speed), SpeedPercent(wenden_speed), .2)
    while True:
        l, m, r = read_vals()
        if (abs(r - m) <= 5 and abs(m - l) <= 5):
            drive.on(SpeedPercent(wenden_speed), SpeedPercent(-wenden_speed))
        else:
            break
    drive.off()


def ziel():
    """Triggers end-of-run and halts loop."""
    global active
    d = us.distance_centimeters - 4
    while d >= 3:
        d = us.distance_centimeters - 4
        forward(40)
    drive.off()
    arm.on_for_rotations(SpeedPercent(10), .5)
    active = False


def forward(speed: int):
    drive.on(SpeedPercent(-speed), SpeedPercent(-speed))


def right():
    drive.on(SpeedPercent(-lenken_speed), SpeedPercent(lenken_speed/4))


def left():
    drive.on(SpeedPercent(lenken_speed/4), SpeedPercent(-lenken_speed))


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


gap_timeout = .5
GAP_THERSHOLD = 10
gap_time = time.time()
was_on_black = True
streifen = 0


def compare(l, m, r, d, t=10):
    """Main decision engine for navigation and barcode detection."""
    global streifen, was_on_black, gap_time

    avg = (l + m + r) / 3
    if d < 15:
        if abs(l - m) <= 10 and abs(m - r) <= 10:
            if d < 20:
                print("vals sind gleichj")
                avg = (l + m + r) / 3
                if avg >= middle_val - 10:
                    return "wenden"
                else:
                    return "ziel"
                    sound.beep()
        return "schranke"

    # -- BARCODE --
    now = time.time()
    on_white = m >= (middle_val - GAP_THERSHOLD)
    if on_white and was_on_black:
        gap_time = now
        streifen += 1
        print(streifen)
        sound.beep()
        was_on_black = False
    elif not on_white:
        was_on_black = True
    if (now - gap_time) > gap_timeout:
        streifen = 0
    if streifen >= 3:
        streifen = 0
        return "schieben"
    # -- BARCODEENDE --

    if m < l - t and m < r - t:
        return "forward"
    if l < r - t:
        return "left"
    if r < l - t:
        return "right"

    return None


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
    elif x == "schieben":
        schieben()
        last_action = "forward"
    else:
        if last_action == "right":
            right()
        elif last_action == "left":
            left()
        elif last_action == "forward":
            forward(speed)


# Main loop execution
loop_count = 0
last_d = 0
while active:
    l, m, r = read_vals()
    # if loop_count % 10 == 0:
    #     loop_count = 0
    last_d = us.distance_centimeters - 2
    a = compare(l, m, r, last_d)
    interpret(a)
    # loop_count += 1
