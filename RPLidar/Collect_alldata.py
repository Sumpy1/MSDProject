#Written by Gopal Pokharel for testing of lidar data in sewer assessment
#This program collects data from RPLidar and sense hat and saves it as a csv file in your Desktop
# Download rplidar package with command "pip install rplidar"
# Download senseHAT package with command "sudo apt-get install sense-hat"
import time
from datetime import datetime
from rplidar import RPLidar
from sense_hat import SenseHat

# Set the path where you want to save the data file
desktop_folder = "/home/pokharelg1/Desktop/"
data_file = desktop_folder + "lidar_data1.csv"

# Initialize the RPLidar scanner
lidar = RPLidar('/dev/ttyUSB0')  # Update the port if necessary

# Initialize the Sense HAT
sense = SenseHat()

# Set the duration in seconds
duration = 20


labels = {
    "timestamp": "Timestamp",
    "quality": "Quality",
    "angle" : "Angle",
    "distance" : "Distance",
    "accel_x": "Acceleration X",
    "accel_y": "Acceleration Y",
    "accel_z": "Acceleration Z",
    "orientation_pitch": "Orientation Pitch",
    "orientation_roll": "Orientation Roll",
    "orientation_yaw": "Orientation Yaw"
}

try:
    # Open the data file for writing
    with open(data_file, 'w') as file:
        header = ", ".join(labels.values())
        file.write(header + "\n")
        # Get the start time
        start_time = time.time()

        # Collect data for the specified duration
        while (time.time() - start_time) < duration:
            # Iterate over each measurement and timestamp
            for scan in lidar.iter_measurments():
                # Get the timestamp or use datetime for current realtime
                timestamp = time.time()-start_time
                #timestamp = datetime.now().strftime("%H:%M:%S.%f")

                # Extract the measurement data
                _, quality, angle, distance = scan

                # Get acceleration data from Sense HAT
                acceleration = sense.get_accelerometer_raw()
                acceleration_x = acceleration['x']
                acceleration_y = acceleration['y']
                acceleration_z = acceleration['z']

                # Get orientation data from Sense HAT
                gyroscope_degrees = sense.get_gyroscope()
                pitch = gyroscope_degrees['pitch']
                roll = gyroscope_degrees['roll']
                yaw = gyroscope_degrees['yaw']

                # Write the data and timestamp to the file
                file.write(f"{timestamp:.3f}, {quality}, {angle:.2f}, {distance}, "
                           f"{acceleration_x:.2f}, {acceleration_y:.2f}, {acceleration_z:.2f}, "
                           f"{pitch:.2f}, {roll:.2f}, {yaw:.2f}\n")

                # Print the data to the console (optional)
                print(f"{timestamp:.3f}, {quality}, {angle:.2f}, {distance:.2f}, "
                      f"{acceleration_x:.2f}, {acceleration_y:.2f}, {acceleration_z:.2f}, "
                      f"{pitch:.2f}, {roll:.2f}, {yaw:.2f}")
                #time.sleep(0.01)

                # Break the loop if the duration has elapsed
                if (time.time() - start_time) >= duration:
                    break

except KeyboardInterrupt:
    print("Program interrupted by the user")

finally:
    # Close the lidar connection
    lidar.stop()
    lidar.disconnect()
