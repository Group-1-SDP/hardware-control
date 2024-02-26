import serial

class NfcReader:
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0',9600) 
    
    def get_reading(self):
        read_serial = self.ser.readline()
        s = str(int(self.ser.readline(),16))
        return s == "1"