'''This program give current local time, seconds elapsed in the day, quality, angle, distance, x and y.
where x and y are cartesian co-ordinates changed from polar(angle,distance). It saves the data as a csv file to
Desktop Folder. Written by Gopal Pokharel for MSD Project'''
import time
from datetime import datetime
from rplidar import RPLidar
import math

# Set the path where you want to save the data file
desktop_folder = "/home/pokharelg1/"
data_file = desktop_folder + "lidar_dataa.csv"

# Initialize the RPLidar scanner
lidar = RPLidar('/dev/ttyUSB0')  # Update the port if necessary

# Set the duration in seconds
duration = 5

def timestamp_to_seconds(timestamp_str):
    # Parse the timestamp string to a datetime object
    time_obj = datetime.strptime(timestamp_str, "%H:%M:%S.%f")

    # Calculate the total number of seconds, including the fractional part
    total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6

    return total_seconds

try:
    # Open the data file for writing
    with open(data_file, 'w') as file:
        # Get the start time
        start_time = time.time()

        # Collect data for the specified duration
        while (time.time() - start_time) < duration:
            # Iterate over each measurement and timestamp
            for scan in lidar.iter_measurments():
                # Get the current timestamp
                timestamp = datetime.now()

                # Extract the measurement data
                _, quality, angle, distance = scan
                #time.sleep(0.1)
                x = (distance * math.cos((angle * (math.pi / 180)))) / 10
                y = (distance * math.sin((angle * (math.pi / 180)))) / 10

                # Format the timestamp to remove the date and convert it to a number
                time_str = timestamp.strftime("%H:%M:%S.%f")[:-2]
                timestamp_number = timestamp_to_seconds(time_str)

                # Get the regular timestamp in "YYYY-MM-DD HH:MM:SS" format
                regular_timestamp = timestamp.strftime("%H:%M:%S.%f")[:-2]

                # Write the data and timestamps to the file
                file.write(f"{regular_timestamp}, {timestamp_number}, {quality}, {angle}, {distance}, {x}, {y}\n")

                # Print the data to the console (optional)
                print(f"{regular_timestamp}, {timestamp_number}, {quality} {angle}, {distance}, {x}, {y}")

                # Break the loop if the duration has elapsed
                if (time.time() - start_time) >= duration:
                    break

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    # Close the lidar connection
    lidar.stop_motor()  #weird thing RPLidar doesn't stop even after giving stop command
    lidar.disconnect()
