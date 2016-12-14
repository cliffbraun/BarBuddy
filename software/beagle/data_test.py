#  Adafruit sensor and logging to CSV. 
#  Modified from "Simple Adafruit BNO055 sensor reading example."

import logging
import sys
import time
from Adafruit_BNO055 import BNO055
import os



bno = BNO055.BNO055(rst='P9_12',busnum=2)

# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')
file_number = 0
while os.path.isfile("/home/Cliff/data_{}.csv".format(file_number)):
    file_number += 1
myfile = open("/home/Cliff/data_{}.csv".format(file_number), 'w')
while True: 
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    start_time = time.time()
    heading, roll, pitch = bno.read_euler()
    # Other values you can optionally read:
    # Sensor temperature in degrees Celsius:
    temp_c = bno.read_temp()
    # Linear acceleration data (i.e. acceleration from movement, not gravity--
    # returned in meters per second squared):
    x,y,z = bno.read_linear_acceleration()
    # Sleep for a second until the next reading.
    myfile.write("{0:0.0F}, {1:0.2F}, {2:0.2F}, {3:0.2F}, {4:0.2F}, {5:0.2F}, {6:0.2F}, {7:0.2F}\n".format(time.time()*1000, heading, roll, pitch, x, y, z, temp_c))
    while (time.time() - start_time) < 0.001:
        time.sleep(0.0001)