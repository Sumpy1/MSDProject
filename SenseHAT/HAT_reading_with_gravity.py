#Written by Gopal(Sumiran Pokharel) for collecting acceleration and orientation values from a Sense HAT
#connected to a raspberry pi

from sense_hat import SenseHat
import time
import os
from datetime import datetime

def collect_data(duration):
    sense = SenseHat()
    start_time = time.time()
    end_time = start_time + duration

    data = []  # List to store the collected data

    while time.time() < end_time:
        accelerometer_raw = sense.get_accelerometer_raw()
        gyroscope_degrees = sense.get_gyroscope()

        data.append({
            'timestamp':datetime.now().strftime("%H:%M:%S.%f"),
            'accel_x': accelerometer_raw['x'],
            'accel_y': accelerometer_raw['y'],
            'accel_z': accelerometer_raw['z'],
            'orientation_pitch': gyroscope_degrees['pitch'],
            'orientation_roll': gyroscope_degrees['roll'],
            'orientation_yaw': gyroscope_degrees['yaw']
        })

        #time.sleep(0.01) # Delay between readings (adjust as needed)
    return data

def save_data_to_file(data, filename):
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    file_path = os.path.join(desktop_path, filename)
    
#file_path = "/home/pi/Desktop/data.txt"
# Example file path, replace with your desired file path

    with open(file_path, 'w') as file:
        for item in data:
            file.write(f"{item['timestamp']},{item['accel_x']:.2f}, {item['accel_y']:.2f}, {item['accel_z']:.2f}, "
                       f"{item['orientation_pitch']:.2f}, {item['orientation_roll']:.2f}, {item['orientation_yaw']:.2f}\n")

    print(f"Data saved to: {file_path}")

# Set the duration for data collection (in seconds)
duration = 5

# Collect accelerometer and orientation data
data = collect_data(duration)

# Save the collected data to a file on the Desktop
save_data_to_file(data, 'data_senseee1.csv')
