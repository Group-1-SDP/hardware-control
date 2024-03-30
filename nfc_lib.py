import serial

#ser = serial.Serial('/dev/ttyACM0',9600)

class NfcReader:
	def __init__(self):
		self.ser = serial.Serial('/dev/ttyACM0',9600)
		

	def get_uid(self):
		uid = self.ser.readline().decode('utf-8').rstrip()
		if uid != '0' and uid != '':
			return '1'
		if uid == ' ':
			return '0'
		return '0'
