from witmotion import IMU
imu = IMU()

print(imu.get_angle())
print(imu.get_acceleration())
print(imu.get_quaternion())

'''Data is not being registered via polling interface and outputs everything as None, I have created a issue on witmotion Github Repository,
check for updates'''