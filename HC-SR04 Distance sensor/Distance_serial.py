"""This program uses serial connection between arduino and raspberry pi to take the distance from HC-SR04
sensor connected to an arduino and takes time-stamps from raspberry pi. Data directly collected by connecting the sensor
to pi had a lot of outliers most probably because of the voltage reduction for the safety of GPIO pins.
Don't connect ultrasonic sensor directly to GPIO pins because it has 5V output voltage which will damage 3v gpio pins.
If you want to connect you have to reduce voltage with resistors or potentiometer
There is also a distance_from_sensor.ino file in this same folder which needs to be compiled and run in arduino
so that it can output data to raspberry pi"""



import serial
import time
import csv
import os
from datetime import datetime

# Replace with the correct serial port (e.g., "/dev/ttyUSB0" or "/dev/ttyACM0")
# You can check serial port by "ls /dev/tty*"
serial_port = "/dev/ttyACM0"

# Function to get the current timestamp in local time with three decimals for seconds
def get_local_timestamp():
    current_time = datetime.now()
    timestamp_str = current_time.strftime("%H:%M:%S.%f")[:-3]
    return timestamp_str

def timestamp_to_seconds(timestamp_str):
    # Parse the timestamp string to a datetime object
    time_obj = datetime.strptime(timestamp_str, "%H:%M:%S.%f")

    # Calculate the total number of seconds elapsed since the start of the day, including the fractional part
    total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6

    return total_seconds

def main():
    # Open the serial port
    ser = serial.Serial(serial_port, 9600)

    try:
        desktop_path = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        filename = os.path.join(desktop_path, "side3.csv")

        with open(filename, mode='w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Regular Timestamp", "Timestamp (Number)", "Distance (cm)"])

            start_time = time.time()

            while True:
                # Read the distance data from the Arduino and split it into two float values
                distance_data = ser.readline().decode().strip()
                try:
                    distance_data = distance_data.split(',')
                    distance1 = float(distance_data[0])
                    distance2 = float(distance_data[1])
                except (ValueError, IndexError):
                    continue

                # Get the regular timestamp with three decimal places for seconds
                regular_timestamp = get_local_timestamp()

                # Get the current timestamp as a number representing seconds elapsed in the day
                current_time_str = get_local_timestamp()
                current_time = timestamp_to_seconds(current_time_str)

                # Write the data to the CSV file
                csv_writer.writerow([regular_timestamp, current_time, distance2])

                # Print the data to the console (optional)
                print(f"{regular_timestamp}, {current_time}, {distance2}")

    except KeyboardInterrupt:
        pass

    finally:
        # Close the serial port
        ser.close()

if __name__ == "__main__":
    main()
