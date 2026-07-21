#!/usr/bin/env python3
"""
Obstacle Challenge - EV3 Robot Navigation System.
This module controls an EV3 robot for navigating an obstacle course
using ultrasonic sensors, a Pixy camera (via I2C), and gyroscope feedback.
"""

import random
import time
from time import sleep

from ev3dev2.button import Button
from ev3dev2.display import Display
from ev3dev2.led import Leds
from ev3dev2.motor import (
    LargeMotor,
    MediumMotor,
    OUTPUT_A,
    OUTPUT_B,
    OUTPUT_D,
)
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import (
    GyroSensor,
    UltrasonicSensor,
)
from ev3dev2.sound import Sound
from smbus import SMBus

# ---------------------------------------------------------------------------
# Device initialization
# ---------------------------------------------------------------------------
btn = Button()
lcd = Display()
speaker = Sound()

# ---------------------------------------------------------------------------
# Ultrasonic sensors (left / right) with error handling
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
        sleep(random.uniform(0, 0.2))
        leds.all_off()
        sleep(random.uniform(0, 0.2))

    raise TypeError("Ultrasonic sensors initialization failed")

# ---------------------------------------------------------------------------
# Pixy camera (I2C) setup
# ---------------------------------------------------------------------------
pixy_port = LegoPort(INPUT_1)
pixy_port.mode = 'other-i2c'
PIXY_ADDRESS = 0x54
i2c_bus = SMBus(3)  # bus for INPUT_1

# ---------------------------------------------------------------------------
# Global state variables
# ---------------------------------------------------------------------------
block = None
loop_counter = 0
base_speed = 90
base_angle = 0
turn_count = 0

# ---------------------------------------------------------------------------
# Motors and sensors
# ---------------------------------------------------------------------------
gyro_sensor = GyroSensor(INPUT_2)
steering_motor = MediumMotor(OUTPUT_B)   # motor_a -> steering
drive_motor = MediumMotor(OUTPUT_D)      # motor_b -> drive
lamp_motor = LargeMotor(OUTPUT_A)

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
    diff = (target_degree - steering_motor.position) * 0.7
    steering_motor.on(clamp(diff, -100, 100))


def get_block(field):
    """
    Extract a field from the Pixy camera block data.

    Parameters
    ----------
    field : str
        One of 'sig', 'x', or 'y'.

    Returns
    -------
    int
        The requested field value, or 0 if no valid object is detected.
    """
    if field == "sig":
        export = block[7] << 8 | block[6]
    elif field == "x":
        export = block[9] << 8 | block[8]
    elif field == "y":
        export = block[11] << 8 | block[10]
    else:
        export = 0

    # If all values are near zero, nothing is detected
    if (
        (block[7] << 8 | block[6]) > 7
        or (block[9] << 8 | block[8]) > 3000
        or (block[11] << 8 | block[10]) > 3000
    ):
        return 0
    return export


# ---------------------------------------------------------------------------
# Gyroscope calibration loop
# ---------------------------------------------------------------------------
sleep(2)
while True:
    try:
        if abs(gyro_sensor.angle) > 2:
            raise ValueError('error')
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
leds.set_color('LEFT', 'GREEN')
leds.set_color('RIGHT', 'GREEN')
lamp_motor.on(100)

# ---------------------------------------------------------------------------
# Determine travel direction based on side distances
# ---------------------------------------------------------------------------
iteration = 0
direction_sum = 0
while iteration != 5:
    right_distance = right_ultrasonic.distance_centimeters
    left_distance = left_ultrasonic.distance_centimeters
    if right_distance > left_distance:
        direction_sum = 1 + direction_sum
    else:
        direction_sum = direction_sum - 1
    iteration = iteration + 1
    sleep(0.02)

direction = 0
if direction_sum > 0:
    direction = 1
    side_ultrasonic = UltrasonicSensor(INPUT_4)
    wall_ultrasonic = UltrasonicSensor(INPUT_3)
    green_line_offset = 120.5
    red_line_offset = 240.5
    side_timing_a = 3
    side_timing_b = 2
else:
    direction = -1
    side_ultrasonic = UltrasonicSensor(INPUT_3)
    wall_ultrasonic = UltrasonicSensor(INPUT_4)
    green_line_offset = 115.5
    red_line_offset = 180
    print("not")
    side_timing_a = 1.5
    side_timing_b = 1

# ---------------------------------------------------------------------------
# Initial movement sequence
# ---------------------------------------------------------------------------
i2c_data = [174, 193, 32, 2, 3, 5]
steering_motor.on_for_seconds((40) * direction, 0.5)
drive_motor.on_for_rotations(80, 0.7)
steering_motor.stop(stop_action='coast')

while True:
    try:
        i2c_bus.write_i2c_block_data(PIXY_ADDRESS, 0, i2c_data)
        break
    except Exception:
        print("khata")

block = i2c_bus.read_i2c_block_data(PIXY_ADDRESS, 0, 20)
lamp_motor.on(100)
sleep(0.5)

Y_IGNORE_THRESHOLD = 80
signature = get_block("sig")
y_position = get_block("y")
if y_position < Y_IGNORE_THRESHOLD:
    signature = 0

# ---------------------------------------------------------------------------
# Signature-based maneuvering (first phase)
# ---------------------------------------------------------------------------
if direction > 0:
    if signature == 0:
        steering_motor.on_for_degrees(100, -steering_motor.position)
        steering_motor.stop(stop_action='coast')
        steering_motor.on_for_degrees(100, 80)
        drive_motor.on_for_rotations(60, 1)
        steering_motor.on_for_degrees(-100, 200)
        drive_motor.on_for_rotations(60, 1.3)
        steering_motor.stop(stop_action='coast')
        steering_motor.on_for_degrees(100, -steering_motor.position)
    elif signature == 2 and y_position > Y_IGNORE_THRESHOLD:
        drive_motor.on_for_degrees(30, 400)
        steering_motor.on_for_seconds(-40, 0.4)
        drive_motor.on_for_rotations(60, 1.5)
        steering_motor.on_for_degrees(40, -steering_motor.position)
        steering_motor.stop(stop_action='coast')
        drive_motor.stop(stop_action='coast')
        print("red")
    elif signature == 1 and y_position > Y_IGNORE_THRESHOLD:
        steering_motor.stop(stop_action='coast')
        steering_motor.on_for_degrees(40, -steering_motor.position)
else:
    if signature == 0:
        steering_motor.on_for_degrees(100, -steering_motor.position)
        steering_motor.stop(stop_action='coast')
        steering_motor.on_for_degrees(-100, 80)
        drive_motor.on_for_rotations(60, 1)
        steering_motor.on_for_degrees(100, 200)
        drive_motor.on_for_rotations(60, 1.3)
        steering_motor.stop(stop_action='coast')
        steering_motor.on_for_degrees(100, -steering_motor.position)
    elif signature == 2 and y_position > Y_IGNORE_THRESHOLD:
        steering_motor.stop(stop_action='coast')
        steering_motor.on_for_degrees(40, -steering_motor.position)
    elif signature == 1 and y_position > Y_IGNORE_THRESHOLD:
        drive_motor.on_for_degrees(30, 400)
        steering_motor.on_for_seconds(40, 0.4)
        drive_motor.on_for_rotations(60, 1.5)
        steering_motor.on_for_degrees(40, -steering_motor.position)
        steering_motor.stop(stop_action='coast')
        drive_motor.stop(stop_action='coast')

# ---------------------------------------------------------------------------
# Main navigation loop
# ---------------------------------------------------------------------------
sleep(0.5)
i2c_data = [174, 193, 32, 2, 3, 5]
last_signature = 0
correction_angle = 0
Y_IGNORE_THRESHOLD = 50
in_straight_segment = True
segment_counter = 0
current_speed = 50
distance_threshold = 1400
zero_reference = 0
turn_start_time = 0
target = 0
last_seen_time = time.time()
drive_motor.reset()
accelerator = base_speed
last_position = 0

while True:
    gyro_value = gyro_sensor.angle * direction
    motor_position = drive_motor.position

    try:
        i2c_bus.write_i2c_block_data(PIXY_ADDRESS, 0, i2c_data)
    except Exception:
        print("khata")
        continue

    block = i2c_bus.read_i2c_block_data(PIXY_ADDRESS, 0, 20)
    signature = get_block("sig")
    y_position = get_block("y")
    x_position = get_block("x")

    if y_position < Y_IGNORE_THRESHOLD:
        signature = 0

    # ----- Signature 1 (green line) -----
    if signature == 1:
        line_estimate = (y_position * 1.1) + green_line_offset  # x=300 y=190
        target = (x_position - line_estimate) * 0.6
        leds.set_color('LEFT', 'GREEN')
        leds.set_color('RIGHT', 'GREEN')
        target = clamp(target, -120, 120)
        steer_to(target)
        last_seen_time = time.time()
        last_position = motor_position

    # ----- Signature 2 (red line) -----
    elif signature == 2:
        line_estimate = (y_position * -1.18) + red_line_offset  # x=25 y=180
        target = (x_position - line_estimate) * 0.6
        leds.set_color('LEFT', 'RED')
        leds.set_color('RIGHT', 'RED')
        target = clamp(target, -120, 120)
        steer_to(target)
        last_seen_time = time.time()
        last_position = motor_position

    else:
        leds.all_off()

    # ----- Wall following using ultrasonic sensors -----
    wall_distance = wall_ultrasonic.distance_centimeters
    side_distance = side_ultrasonic.distance_centimeters
    ultrasonic_output = (55 - wall_distance) * 1.4

    if wall_distance + side_distance < 80 or wall_distance + side_distance > 150:
        ultrasonic_output = 0

    ultrasonic_output = clamp(ultrasonic_output, -45, 45)
    control_output = (((zero_reference + ultrasonic_output + correction_angle) - gyro_value) * 3.2)
    control_output = clamp(control_output, -110, 110)
    steer_to(control_output * direction)

    side_distance = side_ultrasonic.distance_centimeters
    gyro_value = gyro_sensor.angle * direction
    angle_error = abs(zero_reference - gyro_value)

    # ----- Turn detection: right-side open -----
    if side_distance >= 80 and in_straight_segment and correction_angle + angle_error < 20:
        drive_motor.reset()
        distance_threshold = 3400
        turn_count = turn_count + 1
        zero_reference = turn_count * 90
        in_straight_segment = False
        Y_IGNORE_THRESHOLD = 70
        side_timing = side_timing_a
        print("sham")

    # ----- Turn detection: left-side open -----
    if correction_angle + gyro_value > zero_reference + 20 and in_straight_segment and motor_position > distance_threshold:
        drive_motor.reset()
        distance_threshold = 3300
        turn_count = turn_count + 1
        zero_reference = turn_count * 90
        in_straight_segment = False
        Y_IGNORE_THRESHOLD = 70
        side_timing = side_timing_b
        print("mmd")

    # ----- Return to straight segment -----
    if (
        (in_straight_segment is False and side_distance < 80 and angle_error < 25 and motor_position > 1000)
        or (motor_position > 1500 and in_straight_segment is False)
    ):
        segment_counter = segment_counter + 1
        if segment_counter == 7:
            Y_IGNORE_THRESHOLD = 80
            segment_counter = 0
            in_straight_segment = True

    # ----- Speed control -----
    if in_straight_segment or turn_count == 0:
        current_speed = 30
    else:
        current_speed = 70

    if turn_count == 12:
        current_speed = 40
        Y_IGNORE_THRESHOLD = 80

    if turn_start_time == 0:
        turn_start_time = time.time()

    if signature != 0:
        last_signature = signature
    print(last_signature)

    if gyro_value > ((turn_count - 1) * 90) + 60 and signature == 0 and side_timing < time.time() - turn_start_time:
        break

    if current_speed < accelerator:
        accelerator = accelerator - 3
    elif current_speed == accelerator:
        pass
    else:
        accelerator = accelerator + 1

    drive_motor.on(accelerator)

# ---------------------------------------------------------------------------
# Post-loop alignment
# ---------------------------------------------------------------------------
drive_motor.off()
steering_motor.off()
sleep(0.5)
zero_reference = turn_count * 90
drive_motor.reset()
motor_position = 0
steering_motor.on_for_degrees(40, -steering_motor.position)
drive_motor.reset()
correction_angle = 0
Y_IGNORE_THRESHOLD = 80
motor_position = 0

# ---------------------------------------------------------------------------
# Final signature-based alignment
# ---------------------------------------------------------------------------
if direction == 1:
    if last_signature == 1:
        while motor_position < 200:
            gyro_value = gyro_sensor.angle * direction
            drive_motor.on(40)
            motor_position = drive_motor.position
            control_output = ((zero_reference - gyro_value) * 2.2)
            control_output = clamp(control_output, -60, 60)
            steer_to(control_output * direction)
        speaker.beep("-f 1000 -l 20")

    if last_signature == 2:
        while motor_position < 200:
            gyro_value = gyro_sensor.angle * direction
            drive_motor.on(40)
            motor_position = drive_motor.position
            control_output = ((zero_reference - gyro_value) * 2.2)
            control_output = clamp(control_output, -60, 60)
            steer_to(control_output * direction)
        speaker.beep("-f 1000 -l 20")

    if last_signature == 0:
        while motor_position < 600:
            gyro_value = gyro_sensor.angle * direction
            drive_motor.on(40)
            motor_position = drive_motor.position
            control_output = ((zero_reference - gyro_value) * 2.2)
            control_output = clamp(control_output, -60, 60)
            steer_to(control_output * direction)
        speaker.beep("-f 1000 -l 20")

# ---------------------------------------------------------------------------
# Side obstacle negotiation (direction == 1)
# ---------------------------------------------------------------------------
emergency_ultrasonic = UltrasonicSensor(INPUT_4)
side_ultrasonic = UltrasonicSensor(INPUT_3)
drive_motor.reset()
correction_angle = 0
sleep(1)
correction_angle = -36
start_time = time.time()
drive_motor.reset()

while True:
    side_distance = side_ultrasonic.distance_centimeters
    motor_position = drive_motor.position
    gyro_value = gyro_sensor.angle * direction
    leds.all_off()

    control_output = ((((turn_count * 90) - gyro_value) + correction_angle) * 6)
    control_output = clamp(control_output, -100, 100)
    steer_to(control_output)

    ultrasonic_output = (20 - side_distance) * 1.2
    ultrasonic_output = clamp(ultrasonic_output, -45, 45)
    drive_motor.on(20)

    if (side_distance <= 20 and motor_position > 600) or 8 < time.time() - start_time:
        break

# ---------------------------------------------------------------------------
# Reverse alignment
# ---------------------------------------------------------------------------
correction_angle = 0
drive_motor.reset()

while True:
    side_distance = side_ultrasonic.distance_centimeters
    motor_position = drive_motor.position
    gyro_value = gyro_sensor.angle * direction

    ultrasonic_output = (side_distance - 22) * 2
    if side_distance < 10:
        ultrasonic_output = 0

    control_output = (((turn_count * 90) - gyro_value) + (correction_angle + ultrasonic_output)) * 7
    control_output = clamp(control_output, -80, 80)
    steer_to(-control_output)
    drive_motor.on(-20)

    if side_distance < 10 and motor_position < -750:
        break

drive_motor.off()
steering_motor.off()
sleep(0.5)

steering_motor.on_for_degrees(40, -steering_motor.position)
drive_motor.on_for_rotations(10, 0.7)
steering_motor.stop(stop_action='coast')
steering_motor.on_for_degrees(60, -200)
steering_motor.stop()
drive_motor.on_for_degrees(-10, 260)
drive_motor.stop()
steering_motor.stop(stop_action='coast')
steering_motor.on_for_degrees(60, -steering_motor.position)
steering_motor.stop()
sleep(0.3)
drive_motor.on_for_degrees(-10, 90)
drive_motor.off()
sleep(0.3)
drive_motor.reset()

motor_position = 0
while motor_position > -380:
    drive_motor.on(-15)
    motor_position = drive_motor.position
    steer_to((motor_position * -0.8))

drive_motor.stop()
steering_motor.stop(stop_action='coast')
steering_motor.on_for_degrees(60, -steering_motor.position)
steering_motor.stop()
sleep(1)

# ---------------------------------------------------------------------------
# Side obstacle negotiation (direction == -1)
# ---------------------------------------------------------------------------
if direction == -1:
    right_ultrasonic = UltrasonicSensor(INPUT_4)
    left_ultrasonic = UltrasonicSensor(INPUT_3)
    side_distance = 0
    motor_position = 0
    drive_motor.reset()

    if last_signature == 1:
        left_ultrasonic = UltrasonicSensor(INPUT_3)
        while side_distance < 90 or motor_position < 500:
            motor_position = drive_motor.position
            drive_motor.on(40)
            gyro_value = gyro_sensor.angle * direction
            side_distance = left_ultrasonic.distance_centimeters

            ultrasonic_output = (side_distance - 10) * 1.2
            ultrasonic_output = clamp(ultrasonic_output, -50, 50)
            control_output = ((((turn_count * 90) + ultrasonic_output) - gyro_value) * 1.9)
            control_output = clamp(control_output, -50, 50)
            steer_to(control_output * direction)

    else:
        right_ultrasonic = UltrasonicSensor(INPUT_4)
        left_ultrasonic = UltrasonicSensor(INPUT_3)
        left_distance = 0
        while left_distance < 100 or motor_position < 360:
            motor_position = drive_motor.position
            drive_motor.on(40)
            gyro_value = gyro_sensor.angle * direction
            left_distance = left_ultrasonic.distance_centimeters
            side_distance = right_ultrasonic.distance_centimeters

            ultrasonic_output = (32 - side_distance) * 1.2
            ultrasonic_output = clamp(ultrasonic_output, -40, 40)
            control_output = ((((turn_count * 90) + ultrasonic_output) - gyro_value) * 1.9)
            control_output = clamp(control_output, -50, 50)
            steer_to(control_output * direction)

    drive_motor.reset()
    motor_position = 0
    while motor_position < 350:
        gyro_value = gyro_sensor.angle * direction
        drive_motor.on(40)
        motor_position = drive_motor.position
        control_output = ((zero_reference - gyro_value) * 2.2)
        control_output = clamp(control_output, -60, 60)
        steer_to(control_output * direction)
    speaker.beep("-f 1000 -l 20")

    correction_angle = -43
    start_time = time.time()
    drive_motor.reset()
    motor_position = 0

    while True:
        side_distance = right_ultrasonic.distance_centimeters
        motor_position = drive_motor.position
        gyro_value = gyro_sensor.angle * direction
        leds.all_off()

        control_output = ((((turn_count * 90) - gyro_value) + correction_angle) * 6)
        control_output = clamp(control_output, -100, 100)
        steer_to(control_output * direction)

        ultrasonic_output = (18 - side_distance) * 1.2
        ultrasonic_output = clamp(ultrasonic_output, -45, 45)
        drive_motor.on(20)

        if (side_distance <= 20 and motor_position > 200) or 8 < time.time() - start_time:
            break

    correction_angle = 0
    drive_motor.reset()

    while True:
        side_distance = right_ultrasonic.distance_centimeters
        motor_position = drive_motor.position
        gyro_value = gyro_sensor.angle * direction

        ultrasonic_output = (side_distance - 25) * 2
        if side_distance < 10:
            ultrasonic_output = 0

        control_output = (((turn_count * 90) - gyro_value) + (correction_angle + ultrasonic_output)) * 7
        control_output = clamp(control_output, -80, 80)
        steer_to(control_output)
        drive_motor.on(-20)

        if side_distance < 10 and motor_position < -750:
            break

    drive_motor.off()
    steering_motor.off()
    sleep(0.5)

    steering_motor.on_for_degrees(40, -steering_motor.position)
    drive_motor.on_for_rotations(10, 0.75)
    steering_motor.stop(stop_action='coast')
    steering_motor.on_for_degrees(60, 200)
    steering_motor.stop()
    drive_motor.on_for_degrees(-10, 290)
    drive_motor.stop()
    steering_motor.stop(stop_action='coast')
    steering_motor.on_for_degrees(60, -steering_motor.position)
    steering_motor.stop()
    sleep(0.3)
    drive_motor.on_for_degrees(-10, 60)
    drive_motor.off()
    sleep(0.3)
    drive_motor.reset()

    motor_position = 0
    while motor_position > -380:
        drive_motor.on(-15)
        motor_position = drive_motor.position
        steer_to((motor_position * 0.7))

    drive_motor.stop()
    steering_motor.stop(stop_action='coast')
    steering_motor.on_for_degrees(60, -steering_motor.position)
    steering_motor.stop()
    sleep(1)

drive_motor.off()
steering_motor.off()
lamp_motor.stop(stop_action='coast')