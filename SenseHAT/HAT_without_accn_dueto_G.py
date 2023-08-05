#Written by Gopal(Sumiran Pokharel) for collecting acceleration and orientation values from a Sense HAT connected to a raspberry pi
#Used complimentary filter to remove gravity component from accelerometer data
from sense_hat import SenseHat
import time
import os
sense= SenseHat() 
#Enables and disables the magnetometer, gyroscope and/or accelerometer contribution to the get orientation functions below.
#sense.set_imu_config(False, True, False)


labels = {
    "timestamp": "Timestamp",
    "orientation_pitch": "Gyroscope X",
    "orientation_roll": "Gyroscope Y",
    "orientation_yaw": "Gyroscope Z",
    "accel_x": "Acceleration X",
    "accel_y": "Acceleration Y",
    "accel_z": "Acceleration Z"
}

def collect_data(duration):
    start_time = time.time()
    end_time = start_time + duration

    data = []  # List to store the collected data

    while time.time() < end_time:
        accelerometer_raw = sense.get_accelerometer_raw()
        raw = sense.get_gyroscope_raw()
        orientation_radians = sense.get_orientation_radians()

        data.append({
            'timestamp': time.time()-start_time,
            'orientation_pitch': raw['x'], #changing rad/s to deg/s
            'orientation_roll': raw['y'],
            'orientation_yaw': raw['z'],
            'accel_x': accelerometer_raw['x'], 
            'accel_y': accelerometer_raw['y'],
            'accel_z': accelerometer_raw['z']
            
        })

        #time.sleep(0.00000001) # Delay between readings (adjust as needed)
       
    return data


def save_data_to_file(data, filename):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, filename)  
#file_path = "/home/pi/Desktop/data.txt"
# Example file path, replace with your desired file path

    with open(file_path, 'w') as file:
        header = ", ".join(labels.values())
        file.write(header + "\n")
        for item in data:
            data_row = ", ".join([f"{item[key]:.2f}" for key in labels.keys()])
            file.write(data_row + "\n")

    print(f"Data saved to: {file_path}")

# Set the duration for data collection (in seconds)
duration = 40

# Collect accelerometer and orientation data
data = collect_data(duration)

# Save the collected data to a file on the Desktop
save_data_to_file(data, 'SenseData2.csv')

