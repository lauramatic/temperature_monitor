import serial
from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2 import TokenExpiredError
from requests_oauthlib import OAuth2Session
import requests
import datetime


# import all the neccessary libraries

PORT = "/dev/ttyUSB0"
BAUDRATE = "115200"


# define the port and the baudrate

ser = serial.Serial(PORT, BAUDRATE)

class Serial:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.connection = serial.Serial(self.port, self.baudrate, timeout=1)
        self.close = self.connection.close()
        self.open = self.connection.open()

# define a general Serial class


    def read(self, phrase):
        self.connection.write(b"status_get\r\n")
        read_line = self.connection.readline()
        while phrase.encode() not in read_line:
            read_line = self.connection.readline()
        return read_line.decode().split(":")[1].strip()

# define reading of the status package and read until you reach a certain phrase


    def get_uuid(self):
        real_uuid = ""
        counter = 0
        self.connection.write(b"uuid_get\r\n")
        read_line = self.connection.readline()
        while b"UUID" not in read_line:
            read_line = self.connection.readline()
        for a in read_line.decode().split(":")[1].split():
            real_uuid = real_uuid + a[2:]
            counter += 1
            if counter in {4, 6, 8, 10}:
                real_uuid = real_uuid + "-"
        return real_uuid

# get UUID and transform it from RAW to a real UUID number

    def get_gtin(self):
        return self.read("PV2_GTIN")

# get gtin

    def get_firmware(self):
        major = self.read("PV2_FIRMWARE_VERSION_MAJOR")
        minor = self.connection.readline().decode().split(":")[1].strip()
        revision = self.connection.readline().decode().split(":")[1].strip()

        return major + "." + minor + "." + revision

# get FW version, combine the major and minor

    def get_bootloader(self):
        major = self.read("PV2_BOOTLOADER_VERSION_MAJOR")
        minor = self.connection.readline().decode().split(":")[1].strip()
        revision = self.connection.readline().decode().split(":")[1].strip()

        return major + "." + minor + "." + revision

# get the bootloader version, combine the major and minor

    def get_wifi_type(self):
        return self.read("PV2_WIFI_MODULE_ID")[2:]

# get WiFi type

class rma_api:

    def get_access_token(self):
        client_id="C30ifzyuaWQ3HLycDk1eN5meqoUi7M6YIy3eKiW6"
        client = BackendApplicationClient(client_id=client_id)
        client_secret = "gf8zNeFDb275uxN9c7Vzsyh9hq3ATgVVL0lGbziVAqAS72DHZtMEPxNrkGRpMm6ZBrEGZasep8d51TzqxPzdHtQTVZF4AsYwB24U4WCfwQpDgE3heOV5KFKnSN63ulAm"
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url="https://dt.vnct.xyz/api/token/", client_id=client_id, client_secret=client_secret)
        return token["access_token"]

# get access token

    def send_rma(self, data):
        r = requests.post("https://dt.vnct.xyz/api/v1/rma/rma_detail/{}".format(data["device_id"]), json=data, headers={"Authorization": "Bearer " + str(self.get_access_token)})
        print(r.status_code, r.reason)

# send the RMA information using a JSON file

def main():
    rma_information = {}
    user_information = {}
    device_information = []
    command = Serial(PORT, RATE)
    rma_information["id"] = input("Please enter the RMA number: ")
    rma_information["device_id"] = command.get_uuid()
    print(rma_information["device_id"])
    rma_information["date_recieved"] = datetime.datetime.now().isoformat()
    device_information.extend((command.get_gtin(), command.get_firmware(), command.get_bootloader(), command.get_wifi_type()))
    print("RMA information. Make sure you press enter after each input.\n")
    print("Reasons for return:\n15: Integration\n14: Damage-wifi\n13: Damage-screen\n12: Upgrade\n9: CC signal\n8: Battery\n7: Satisfied\n5: Costs\n4: RS module\n3: CC module")
    rma_information["return_reason"] = input("Select return reason: ")
    print("State of the RMA at this moment:\n6: Open\n7: Closed\n8: In transit\n9: At customs\n10: Arrived\n11: Testing\n12: Repair")
    rma_information["return_state"] = input("Select the state of the RMA: ")
    user_information["customer_name"] = input("Please enter the customers name: ")
    user_information["customer"] = input("Please enter the customers email: ")
    user_information["country"] = input("Please enter the customers country: ")
    user_information["company_name"] = input("Please enter the customers company name: ")


    send_data = Rma_api()
    send_data.send_rma(rma_information)

# import the device information and insert the customer information and the RMA information


if __name__ == '__main__':
    main()