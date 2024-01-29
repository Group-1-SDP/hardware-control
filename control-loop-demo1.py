import os
import time

task_signal = 0

# get inputs

dispenser_connected = False
phone_in = True #temp

if dispenser_connected:
    while True:
        #get inputs
        match (task_signal):
            case 1:
                #dispense
            case 2:
                #dispense
            case 3:
                #dispense
            case 4:
                #dispense
            case _:
                time.sleep(1)

else:
    while True:
        #get inputs
        match (task_signal):
            case 1:
                # jingle
            case 2:
                # jingle
            case 3:
                # jingle
            case 4:
                # jingle
            case _:
                time.sleep(1)