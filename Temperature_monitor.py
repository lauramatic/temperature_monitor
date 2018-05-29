import serial, datetime


ser = serial.Serial("/dev/ttyUSB0", "115200")         # open serial port
print(ser.name)                                       # check which port was really used

ser.write("status_get\r\n")                           # input command status_get

read_line = ser.readline()
while("PV2_EPD_TEMP_SENSOR" not in read_line):        # read until it comes across the temperature
    read_line = ser.readline()
    if "PV2_EPD_TEMP_SENSOR" in read_line:
        temp = read_line.split(":")[1]
        print("Temperature at {1} was {0} degrees celsius".format(temp.strip(), datetime.datetime.today().isoformat()))
        return(temp.strip(),datetime.datetime.today().isoformat())
ser.close()
