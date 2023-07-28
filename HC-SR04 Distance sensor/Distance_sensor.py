import RPi.GPIO as GPIO
import time
import csv
import os
from datetime import datetime

GPIO.setmode(GPIO.BCM)

TRIG = 23
ECHO = 24

print('Distance and Timestamp printing')

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.00000000000000000001)

    GPIO.output(TRIG, True)
    time.sleep(0.00000000001)
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

def timestamp_to_seconds(timestamp_str):
    # Parse the timestamp string to a datetime object
    time_obj = datetime.strptime(timestamp_str, "%H:%M:%S.%f")

    # Calculate the total number of seconds, including the fractional part
    total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6

    return total_seconds

try:
    desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    filename = os.path.join(desktop_path, "Distance_data.csv")

    with open(filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Regular Timestamp", "Timestamp (Number)", "Distance (cm)"])

        start_time = time.time()

        while True:
            distance = get_distance()

            # Get the regular timestamp with three decimals for seconds
            regular_timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]

            # Get the current timestamp as a number representing seconds elapsed in the day
            current_time_str = datetime.now().strftime("%H:%M:%S.%f")
            current_time = timestamp_to_seconds(current_time_str)

            csv_writer.writerow([regular_timestamp, current_time, distance])
            print(f"{regular_timestamp}, {current_time}, {distance}")

except KeyboardInterrupt:
    print("Measurement stopped by the user")

finally:
    GPIO.cleanup()
