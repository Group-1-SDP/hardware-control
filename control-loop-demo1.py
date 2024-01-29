import sys
import time
import nfc

task_signal = 1

# get inputs

#phone_reader = nfc.ContactlessFrontend('replace me')

def Body():

    while True:
        phone_connected = True #sys.argv[1]

        while phone_connected:
            dispenser_connected = False #sys.argv[2]

            if dispenser_connected:
                #get inputs
                match (task_signal):
                    case 1:
                        print("dispense")
                    case 2:
                        print("dispense")
                    case 3:
                        print("dispense")
                    case 4:
                        print("dispense")
                    case _:
                        time.sleep(1)
            else:
                #get inputs
                match (task_signal):
                    case 1:
                        print("jingle")
                    case 2:
                        print("jingle")
                    case 3:
                        print("jingle")
                    case 4:
                        print("jingle")
                    case _:
                        time.sleep(1)
            # delay for input signal changes
        while not phone_connected:
            phone_connected = IsPhoneConnected()

    # power off code



def IsDispenserConnected(args):
    return args[1]

def IsPhoneConnected(args):
    return args[0]

if __name__ == "__main__":
    Body()