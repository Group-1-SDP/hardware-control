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
                if task_signal == 1:
                    print("dispense")
                elif task_signal == 2:
                    print("dispense")
                elif task_signal == 3:
                    print("dispense")
                elif task_signal == 4:
                    print("dispense")
                else:
                    time.sleep(1)
            else:
                #get inputs
                if task_signal == 1:
                    print("jingle")
                elif task_signal == 2:
                    print("jingle")
                elif task_signal == 3:
                    print("jingle")
                elif task_signal == 4:
                    print("jingle")
                else:
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