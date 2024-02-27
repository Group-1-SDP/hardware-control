import curses
import requests
import time
from nfc import NfcReader
import grove_servo 
import threading # threading? really?
# Yes. The timer needs to constantly run, but the text needs to scroll
# independently of the timer. This allows two seperate time.sleep() calls
# to update different aspects of the screen at different rates.
# This will also be used to handle our concurrency for integrati
import socketio 

time_in_secs = 0

def sevenSegmentASCII(num):
    """Function that returns an ASCII representation of the time in seven segment display style"""
    zero = """
     $$$$$$ 
    $$$   $$
    $$$$  $$
    $$ $$ $$
    $$  $$$$
    $$   $$$
     $$$$$$ 
    """
    one = """
      $$  
    $$$$  
      $$  
      $$  
      $$  
      $$  
    $$$$$$
    """
    two = """
     $$$$$$ 
    $$    $$
          $$
     $$$$$$ 
    $$      
    $$      
    $$$$$$$$
    """
    three = """
     $$$$$$ 
    $$    $$
          $$
      $$$$$ 
          $$
    $$    $$
     $$$$$$ 
    """
    four = """
    $$    $$
    $$    $$
    $$    $$
    $$$$$$$$
          $$
          $$
          $$
    """
    five = """
    $$$$$$$ 
    $$      
    $$      
    $$$$$$$ 
          $$
    $$    $$
     $$$$$$ 
    """
    six = """
     $$$$$$ 
    $$    $$
    $$      
    $$$$$$$ 
    $$    $$
    $$    $$
     $$$$$$ 
    """
    seven = """
    $$$$$$$$
         $$ 
        $$  
       $$   
      $$    
     $$     
    $$      
    """
    eight = """
     $$$$$$ 
    $$    $$
    $$    $$
     $$$$$$ 
    $$    $$
    $$    $$
     $$$$$$ 
    """
    nine = """
     $$$$$$ 
    $$    $$
    $$    $$
     $$$$$$$
          $$
    $$    $$
     $$$$$$ 
    """
    digits = [zero, one, two, three, four, five, six, seven, eight, nine]
    return digits[num]

colon = """
      
   ***
   ***
      
   ***
   ***
      
    """

def nums_side_by_side(*args):
    lines = [arg.split('\n') for arg in args]

    # Get the maximum number of lines
    max_lines = max(len(line) for line in lines)

    array_of_lines = []
    # Print each line side by side
    for i in range(max_lines):
        line_parts = []
        for line in lines:
            if i < len(line):
                line_parts.append(line[i])
        array_of_lines.append(''.join(line_parts))
    return array_of_lines


def update_time(stop_event, start_time):
    global time_in_secs
    while not stop_event.is_set():
        time_in_secs = int(time.time() - start_time)
        time.sleep(1)

def update_display(stdscr, stop_event):
    global time_in_secs
    while not stop_event.is_set():
        timer = time.strftime("%M:%S", time.gmtime(time_in_secs))
        digit1 = int(timer[0])
        digit2 = int(timer[1])
        digit3 = int(timer[3])
        digit4 = int(timer[4])
        time_line_array = nums_side_by_side(sevenSegmentASCII(digit1), sevenSegmentASCII(digit2), colon, sevenSegmentASCII(digit3), sevenSegmentASCII(digit4))

        # Start of screen stuff
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(1, 1,  '*****************************************************')
        stdscr.addstr(2, 1,  '*                     Time on task                  *')
        stdscr.addstr(3, 1,  '*****************************************************')
        stdscr.addstr(4, 1,  time_line_array[1])
        stdscr.addstr(5, 1,  time_line_array[2])
        stdscr.addstr(6, 1,  time_line_array[3])
        stdscr.addstr(7, 1,  time_line_array[4])
        stdscr.addstr(8, 1,  time_line_array[5])
        stdscr.addstr(9, 1,  time_line_array[6])
        stdscr.addstr(10, 1, time_line_array[7])
        stdscr.addstr(11, 1, '*****************************************************')

        stdscr.refresh()
        time.sleep(1)

def display_time(stdscr, phone_connected, nfcReader):
    curses.curs_set(0)
    stdscr.nodelay(True) # Stop getch() from blocking program execution

    messages = {
        '1': "Phone connected",
        '2': "Phone disconnected",
        '3': "Pavel just completed 10 tasks!",
        '4': "New task added: 'Impress judges at Demo 1!'"
    }

    threads = []
    stop_events = []

    start_time = time.time()
    stop_event = threading.Event()

    time_thread = threading.Thread(target=update_time, args=(stop_event, start_time))
    display_thread = threading.Thread(target=update_display, args=(stdscr, stop_event))
    time_thread.start()
    display_thread.start()

    while nfcReader.get_reading():
        # Convert time_in_secs to minutes and seconds

        global time_in_secs


    stop_event.set()
    time_thread.join()
    display_thread.join()

def draw_menu(stdscr):
    phone_connected = False
    dispenser_connected = False
    task_signal = 1
    k = 0
    url="https://studious-lamp-p45x777q9rp27gx5-5000.app.github.dev/websocket/"

    stdscr.nodelay(1)

    sio = socketio.Client()
    sio.connect('https://fantastic-broccoli-p6jp6jjvpvwhrj5x-5000.app.github.dev/')

    tasks = []

    # init nfc reader

    nfcReader = NfcReader()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while k != ord('q'):  # Press 'q' to exit
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        event = sio.receive()

        # Handle input

        if nfcReader.get_reading():
            phone_connected = True
            requests.post(url + "phoneConnected")
            display_time(stdscr, phone_connected, nfcReader)
        else:
            phone_connected = False
            requests.post(url + "phoneDisconnected")

        if k == ord('d'):
            dispenser_connected = not dispenser_connected
        elif ord('0') <= k <= ord('4'):
            task_signal = k - ord('0')
        elif k == ord('z'):
            task = add_task(stdscr)
            tasks.append(task)

        if dispenser_connected:
            if event[0] == 'task-completed':
                grove_servo.main()

        # Render the UI
        stdscr.addstr(1, 1, '**************************************************')
        stdscr.addstr(2, 1, '*                                                *')
        stdscr.addstr(3, 1, '*  Phone connected: [{:<5}]                      *'.format(str(phone_connected)))
        stdscr.addstr(4, 1, '*  Dispenser connected: [{:<5}]                  *'.format(str(dispenser_connected)))
        stdscr.addstr(5, 1, '*  Task signal: [{:<5}]                          *'.format(task_signal))
        stdscr.addstr(6, 1, '*  Tasks:                                        *')
        stdscr.addstr(7, 1, '* "d" toggles dispenser connection               *')
        stdscr.addstr(8, 1, '* Press "q" to quit                              *')
        stdscr.addstr(9, 1, '* Numbers 0-4 change task, "s" does task pulse   *')
        stdscr.addstr(10, 1,'*                                                *')
        if phone_connected == True:
            stdscr.addstr(11, 1,'*   _______                                      *')
            stdscr.addstr(12, 1,'*  |       |             /                       *')
            stdscr.addstr(13, 1,'*  |       |            /                        *')
            stdscr.addstr(14, 1,'*  |       |           /                         *')
            stdscr.addstr(15, 1,'*  |       |     \    /                          *')
            stdscr.addstr(16, 1,'*  |       |      \  /                           *')
            stdscr.addstr(17, 1,'*  |_______|       \/                            *')
        else:
            for i in range(11, 18):
                stdscr.addstr(i, 1,'*                                                *')
        stdscr.addstr(18, 1,'*                                                *')
        stdscr.addstr(19, 1,'**************************************************')
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        # Send pulse if 's' is pressed
        if k == ord('s'):
            perform_action(stdscr, height, width, phone_connected, dispenser_connected, task_signal)

def main(): 
    curses.wrapper(draw_menu)

if __name__ == "__main__":    
    main()




''' keypress = stdscr.getch()
if keypress == ord('q'):
    # Signal all threads to stop
    for event in stop_events:
        event.set()
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    break
elif keypress in (ord('1'), ord('2'), ord('3'), ord('4')):
    # I would love to use "if chr(keypress) in messages" but that causes
    # a stupid chr error. This is the best workaround, which sucks.

    # threading
    stop_event = threading.Event()
    stop_events.append(stop_event)
    # more threading
    message_key = chr(keypress)
    new_thread = threading.Thread(target=scroll_text_line, args=(stdscr, 2, 2, width-1, messages[message_key], 20, stop_event))
    threads.append(new_thread)
    new_thread.start()'''