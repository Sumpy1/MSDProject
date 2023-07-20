'''Collects and stores witmotion data on Desktop, data collection through polling
interface is not working so I have used callback function.'''
import os
import logging
from witmotion import IMU

def callback(msg):
    logging.info(msg)

# Get the path to the user's desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Define the file name for saving the output
output_file = os.path.join(desktop_path, "output.csv")

# Configure logging to save messages to the file
logging.basicConfig(filename=output_file, level=logging.INFO, format='%(message)s')

imu = IMU()
imu.subscribe(callback)
