import datetime
from time import time
import serial
import matplotlib.pyplot as plt


# database location
dbname = "Temperaturelog.db"

# for graphs

plt.ion()
x = []
y = []

# serial device

BAUDRATE = "115200"
PORT = "/dev/ttyUSB0"

ser = serial.Serial(PORT, BAUDRATE)

# timeout in second for waiting to read the temperature

TIMEOUT = 10

class Visionect:
    def __init__(self, port, rate):
        self.port = port
        self.rate = rate
        self.connection = serial.Serial(self.port, self.rate, timeout=1)
        self.close = self.connection.close()
        self.open = self.connection.open()

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

    # def graph(temp):
    # y.append(temp)
    # x.append(time())
    # plt.clf()
    # plt.scatter(x, y)
    # plt.plot(x, y)
    # plt.draw()

d1 = Visionect(PORT, BAUDRATE)
print d1.get_temperature()

#class Reading:
    #def __init__(self, temperature, date):
        #self.temperature = temperature
        #self.date = date

#with open("Temperature.csv", "a") as log:
    #while True:
        #temp = temperature
        #log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"), str(temp)))
        #time.time.sleep(10) # read every 10 seconds
        #timeout = time.time.time() + 60 * 5 #Timeout 5 minutes from now







# define class Reading with temperature and date as their attributes
# read temperature for 5 minutes and save values to list
# result: [temp1, temp2, temp3,...]



#list_name = [ ]
#user_input = raw_input("Tell user to enter value") #use this to input the RMA and customer info
