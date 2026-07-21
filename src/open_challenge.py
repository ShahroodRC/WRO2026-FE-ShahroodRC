#!/usr/bin/env python3
"""
Open Challenge - EV3 Robot Navigation System (Simplified).
This module controls an EV3 robot for open field navigation using
ultrasonic sensors and gyroscope feedback.
"""

import random
import time
from time import sleep

from ev3dev2.button import Button
from ev3dev2.display import Display
from ev3dev2.led import Leds
from ev3dev2.motor import MediumMotor, OUTPUT_B, OUTPUT_D
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor
from ev3dev2.sound import Sound

# ---------------------------------------------------------------------------
# Device initialization
# ---------------------------------------------------------------------------
lcd = Display()
speaker = Sound()
btn = Button()

# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------
turn_count = 0

# ---------------------------------------------------------------------------
# Sensor initialization with error handling
# ---------------------------------------------------------------------------
try:
    left_ultrasonic = UltrasonicSensor(INPUT_3)
    right_ultrasonic = UltrasonicSensor(INPUT_4)
except Exception:
    leds = Leds()
    leds.all_off()

    start_time = time.time()
    while time.time() - start_time < 20:
        leds.set_color('LEFT', 'RED')
        leds.set_color('RIGHT', 'RED')

    while not btn.enter:
        leds.all_off()
        lcd.update()
        lcd.clear()
        sleep(5)

    start_time = time.time()
    while time.time() - start_time < 10:
        leds.set_color('LEFT', 'ORANGE')
        leds.set_color('RIGHT', 'ORANGE')
        random_sleep = random.uniform(0, 0.2)
        sleep(random_sleep)
        leds.all_off()
        random_sleep = random.uniform(0, 0.2)
        sleep(random_sleep)

    raise TypeError("Ultrasonic sensors not found")

# ---------------------------------------------------------------------------
# Motors and sensors
# ---------------------------------------------------------------------------
gyro_sensor = GyroSensor(INPUT_2)
steering_motor = MediumMotor(OUTPUT_B)
drive_motor = MediumMotor(OUTPUT_D)

steering_motor.reset()
drive_motor.reset()

gyro_sensor.mode = 'GYRO-RATE'
sleep(0.1)
gyro_sensor.mode = 'GYRO-ANG'
sleep(0.1)
gyro_sensor.reset()
sleep(2)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def clamp(value, minimum, maximum):
    """Clamp a value between minimum and maximum bounds."""
    if value > maximum:
        value = maximum
    if value < minimum:
        value = minimum
    return value


def steer_to(target_degree):
    """Adjust steering motor to target degree using proportional control."""
    diff = (target_degree - steering_motor.position) * 2
    steering_motor.on(clamp(diff, -100, 100))


# ---------------------------------------------------------------------------
# Gyroscope calibration loop
# ---------------------------------------------------------------------------
sleep(2)
while True:
    try:
        if abs(gyro_sensor.angle) > 5:
            raise ValueError('begaii')
        speaker.beep("-f 300 -l 50")
        break
    except Exception:
        speaker.beep("-f 1000 -l 500")
        gyro_sensor.mode = 'GYRO-CAL'
        sleep(1)
        gyro_sensor.mode = 'GYRO-ANG'
        sleep(2)


# ---------------------------------------------------------------------------
# Initial LED indication
# ---------------------------------------------------------------------------
leds = Leds()
leds.set_color('LEFT', 'ORANGE')
leds.set_color('RIGHT', 'ORANGE')

# btn.wait_for_bump('left')
leds.set_color('LEFT', 'GREEN')
leds.set_color('RIGHT', 'GREEN')

# ---------------------------------------------------------------------------
# Initial alignment phase
# ---------------------------------------------------------------------------
correction_angle = 0
right_distance = 0
left_distance = 0

while left_distance < 100 and right_distance < 100:
    gyro_value = gyro_sensor.angle
    control_output = -gyro_value * 2.2
    control_output = clamp(control_output, -90, 90)
    steer_to(control_output)

    right_distance = right_ultrasonic.distance_centimeters
    left_distance = left_ultrasonic.distance_centimeters
    drive_motor.on(100)

# ---------------------------------------------------------------------------
# Determine travel direction based on side distances
# ---------------------------------------------------------------------------
if right_distance > 100:
    direction = 1
    side_ultrasonic = UltrasonicSensor(INPUT_4)
elif left_distance > 100:
    direction = -1
    side_ultrasonic = UltrasonicSensor(INPUT_3)

turn_count = 1
drive_motor.reset()

# ---------------------------------------------------------------------------
# Main navigation loop
# ---------------------------------------------------------------------------
while True:
    gyro_value = gyro_sensor.angle * direction
    side_distance = side_ultrasonic.distance_centimeters

    control_output = side_distance - 10
    if side_distance > 60:
        control_output = 0

    control_output = (
        ((turn_count * 90) + (correction_angle + control_output) - gyro_value) * 2.2
    )
    control_output = clamp(control_output, -90, 90)
    steer_to(control_output * direction)

    if side_distance > 80 and drive_motor.position > 2000:
        correction_angle = 90

    if gyro_value > (turn_count * 90) + 65:
        correction_angle = 0
        turn_count = turn_count + 1
        drive_motor.reset()
        print(turn_count)

    drive_motor.on(100)
    if turn_count == 12:
        break

# ---------------------------------------------------------------------------
# Final alignment phase
# ---------------------------------------------------------------------------
correction_angle = 0
drive_motor.reset()

while drive_motor.position < 1000:
    gyro_value = gyro_sensor.angle * direction
    drive_motor.on(100)
    control_output = ((turn_count * 90) + correction_angle - gyro_value) * 2.2
    control_output = clamp(control_output, -60, 60)
    steer_to(control_output * direction)

drive_motor.off()
steering_motor.off()