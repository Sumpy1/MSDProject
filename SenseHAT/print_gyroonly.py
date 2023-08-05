from sense_hat import SenseHat

sense = SenseHat()
while True:
    gyro_only = sense.get_gyroscope()
    print("p: {pitch:.2f}, r: {roll:.2f}, y: {yaw:.2f}".format(**gyro_only))
    
    