import serial
import datetime

BAUDRATE = "115200"

class Visionect:
    def __init__(self, port, rate):
        self.port = port
        self.rate = rate

    def open(self):
        pass

    def close(self):
        pass

    def get_temperature(self):
        ser = serial.Serial(self.port, self.rate)             # open serial port
        print(ser.name)                                       # check which port was really used

        ser.write("status_get\r\n")                           # input command status_get

        read_line = ser.readline()
        while("PV2_EPD_TEMP_SENSOR" not in read_line):        # read until it comes across the temperature
            read_line = ser.readline()


        temp = read_line.split(":")[1]                        # split to get just the temperature
        print("Temperature at {1} was {0} degrees celsius".format(temp.strip(), datetime.datetime.today().isoformat()))

        ser.close()
        return temp.strip(), datetime.datetime.today().isoformat()

d1 = Visionect("/dev/ttyUSB0", BAUDRATE)
print d1.get_temperature()

# define class Reading with temperature and date as their attributes
# read temperature for 5 minutes and save values to list
# result: [temp1, temp2, temp3,...]