import RPi.GPIO as GPIO
import time
import csv
import os

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print('Distance and Timestamp printing')

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.0000000001)

    GPIO.output(TRIG, True)
    time.sleep(0.00000001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(ECHO) == 0 and pulse_start - pulse_end < 0.1:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1 and pulse_end - pulse_start < 0.1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

try:
    desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    filename = os.path.join(desktop_path, "Distance_data.csv")

    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Timestamp", "Distance (cm)"])

        start_time = time.time()

        while True:
            distance = get_distance()

            # Get the current timestamp with three decimal points for milliseconds
            current_time = time.time()
            formatted_time = time.strftime("%H:%M:%S", time.localtime(current_time))
            timestamp_ms = round((current_time - int(current_time)) * 1000)
            current_time = f"{formatted_time}.{timestamp_ms:03}"

            csv_writer.writerow([current_time, distance])
            print(f" {distance} cm, {current_time}")

except KeyboardInterrupt:
    print("Measurement stopped by the user")

finally:
    GPIO.cleanup()
