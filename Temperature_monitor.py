# import serial library
import serial
ser = serial.Serial('/dev/ttyUSB0')         # open serial port
print(ser.name)                             # check which port was really used

ser.write("sudo minicom -D /dev/ttyUSB0")   # open minicom
ser.write()                                 # enter password
ser.write("status_get")                     # gets the status of the device
read_data = ser.read(13)                    # read line 13 - PV2_MIN_TEMPERATURE
# response = ser.readline()
print("Data received : " + read_data)