import curses
import requests
import time
from nfc_lib import NfcReader
import threading
import socketio
import grove_servo
import notification_detection.ocr_pi 
from notification_detection.text_filter import TextFilter
from notification_detection.ocr_pi import OCR

#we need threading to run the time and the display at the same time; otherwise there will be noticeable lag.

time_in_secs = 0
text_filter = TextFilter()
ocr = OCR()

tick_current = 4 
start_tick = time.time()
tick_timer = start_tick
display_tickagotchi = False

url="https://obscure-invention-4x774xpv7fqxqx-5000.app.github.dev/websocket/"

sio = socketio.Client()
conn = False
while conn == False:
    try:
        sio.connect(url)
        conn = True
    except Exception as e:
        print("Connection failed. Retrying in two seconds...")
        time.sleep(2)

@sio.on('task-complete')
def on_task_complete():
    global tick_timer
    global start_tick
    global tick_current
    if tick_current < 4:
        tick_current += 1
    start_tick = time.time()
    tick_timer = start_tick

@sio.on('timer-done')
def on_timer_done():
    #print("HASILDHI")
    grove_servo.main()

@sio.on('detect-notifications')
def detect_notifications():
    ocr.start(text_filter)
#    thread = threading.Thread(target=ocr.run, args=(text_filter,))
#    thread.start()

@sio.on('stop-detecting')
def stop_detecting():
    ocr.terminate()
#    ocr.terminate()

@sio.on('tickagotchi')
def tickagotchi():
    global display_tickagotchi
    display_tickagotchi = not display_tickagotchi

def seven_segment(num):
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
    $$$$  
  $$$$$$  
     $$$  
     $$$  
     $$$  
     $$$  
  $$$$$$$$
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

def update_tick_time(stop_event):
    global tick_timer
    global start_tick
    global tick_current
    while not stop_event.is_set():
        tick_timer = int(time.time() - start_tick)
        if tick_timer > 10 and tick_current > 0:
            tick_current -= 1
            start_tick = time.time()
            tick_timer = start_tick
        time.sleep(1)

def update_display(stdscr, stop_event):
    global time_in_secs
    while not stop_event.is_set():
        timer = time.strftime("%M:%S", time.gmtime(time_in_secs))
        digit1 = int(timer[0])
        digit2 = int(timer[1])
        digit3 = int(timer[3])
        digit4 = int(timer[4])
        time_line_array = nums_side_by_side(seven_segment(digit1), seven_segment(digit2), colon, seven_segment(digit3), seven_segment(digit4))

        # Start of screen stuff
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(1, 1,  '**************************************************')
        stdscr.addstr(2, 1,  '*                Time on task                    *')
        stdscr.addstr(3, 1,  '**************************************************')
        stdscr.addstr(4, 1,  '*' + time_line_array[1] + '   *')
        stdscr.addstr(5, 1,  '*' + time_line_array[2] + '   *') 
        stdscr.addstr(6, 1,  '*' + time_line_array[3] + '   *')
        stdscr.addstr(7, 1,  '*' + time_line_array[4] + '   *')
        stdscr.addstr(8, 1,  '*' + time_line_array[5] + '   *')
        stdscr.addstr(9, 1,  '*' + time_line_array[6] + '   *')
        stdscr.addstr(10, 1, '*' + time_line_array[7] + '   *')
        stdscr.addstr(11, 1, '*                                                *')
        spaces_notif = ' ' * ((48-len(text_filter.text_to_display))//2)
        odd_case = (' ' if (48-len(text_filter.text_to_display)) % 2 != 0 else '')
        stdscr.addstr(12, 1, "*" + spaces_notif + f'{text_filter.text_to_display}' +  spaces_notif + odd_case + "*")
        for i in range(13, 19):
            stdscr.addstr(i, 1, '*                                                *')
        stdscr.addstr(19, 1, '**************************************************')

        stdscr.refresh()
        time.sleep(1)

def display_time(stdscr, phone_connected, nfcReader):
    curses.curs_set(0)
    stdscr.nodelay(True)

    start_time = time.time()
    stop_event = threading.Event()

    time_thread = threading.Thread(target=update_time, args=(stop_event, start_time))
    display_thread = threading.Thread(target=update_display, args=(stdscr, stop_event))
    time_thread.start()
    display_thread.start()

    while nfcReader.get_uid() != '0':
        pass

    stop_event.set()
    time_thread.join()
    display_thread.join()

def draw_menu(stdscr):

    global tick_current
    global display_tickagotchi 
    phone_connected = False

    stdscr.nodelay(True)
    curses.curs_set(0)
    
    # init nfc reader

    nfcReader = NfcReader()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    #start tickagotchi background timekeeping
    stop_event = threading.Event()

    tick_time_thread = threading.Thread(target=update_tick_time, args=(stop_event, ))
    tick_time_thread.start()

    while True:
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if nfcReader.get_uid() == '1' and phone_connected == False :
            phone_connected = True
            requests.post(url + "phoneConnected")
            display_time(stdscr, phone_connected, nfcReader)
        elif nfcReader.get_uid() != '1' and phone_connected == True:
            phone_connected = False
            requests.post(url + "phoneDisconnected")

        # Render the UI
        if display_tickagotchi == False and phone_connected == False:
            stdscr.addstr(1, 1, '**************************************************')
            stdscr.addstr(2, 1, '*                   TickBox                      *')
            stdscr.addstr(3, 1, '*             Please connect a phone             *')
            stdscr.addstr(4, 1, '**************************************************')
            stdscr.addstr(5, 1, '*                                                *')
            stdscr.addstr(6, 1, '*                                                *')
            stdscr.addstr(7, 1, '*                  $$$$$$$$$$$                   *')
            stdscr.addstr(8, 1, '*                  $    %    $                   *')
            stdscr.addstr(9, 1, '*                  $         $                   *')
            stdscr.addstr(10, 1,'*   $$$$$$$$$      $         $                   *')
            stdscr.addstr(11, 1,'*           $      $         $                   *')
            stdscr.addstr(12, 1,'*           $      $         $                   *')
            stdscr.addstr(13, 1,'*   $$$$$$$ $      $         $                   *')
            stdscr.addstr(14, 1,'*         $ $      $         $                   *')
            stdscr.addstr(15, 1,'*   $$$$  $ $      $$$$$$$$$$$                   *')
            stdscr.addstr(16, 1,'*      $  $ $      $    %    $                   *')
            stdscr.addstr(17, 1,'*   $  $  $ $      $$$$$$$$$$$                   *')
            stdscr.addstr(18, 1,'*                                                *')
            stdscr.addstr(19, 1,'**************************************************')
        #elif display_tickagotchi == True:
        while display_tickagotchi:
        
            if tick_current == 4:
                stdscr.addstr(1, 1, '**************************************************')
                stdscr.addstr(2, 1, '*                   TickBox                      *')
                stdscr.addstr(3, 1, '*                 Tickagotchi                    *')
                stdscr.addstr(4, 1, '**************************************************')
                stdscr.addstr(5, 1, '*    $$$$$$$  $$$$$$$$$$$$$$$  $$$$$$$           *')
                stdscr.addstr(6, 1, '*  $$       $$               $$       $$         *')
                stdscr.addstr(7, 1, '* $          /---         ---\          $        *')
                stdscr.addstr(8, 1, '*$          $ $$           $$ $          $       *')
                stdscr.addstr(9, 1, '* $   $$    $$  $         $  $$    $$   $        *')
                stdscr.addstr(10, 1,'*  $ $  $   $ $$           $$ $   $  $ $         *')
                stdscr.addstr(11, 1,'*   $    $  $                 $  $    $          *')
                stdscr.addstr(12, 1,'*         $ $      $$$$$      $ $                *')
                stdscr.addstr(13, 1,'*           $       $$$       $                  *')
                stdscr.addstr(14, 1,'*           $        $        $                  *')
                stdscr.addstr(15, 1,'*            $    $$$$$$$    $                   *')
                stdscr.addstr(16, 1,'*             $    $___$    $                    *')
                stdscr.addstr(17, 1,'*              $$         $$                     *')
                stdscr.addstr(18, 1,'*                $$$$$$$$$                       *')
                stdscr.addstr(19, 1,'**************************************************')
            if tick_current == 3:
                stdscr.addstr(1, 1, '**************************************************')
                stdscr.addstr(2, 1, '*                   TickBox                      *')
                stdscr.addstr(3, 1, '*                 Tickagotchi                    *')
                stdscr.addstr(4, 1, '**************************************************')
                stdscr.addstr(5, 1, '*          $$$$$$$$$$$$$$$                       *')
                stdscr.addstr(6, 1, '*        $$               $$                     *')
                stdscr.addstr(7, 1, '*       $ /---         ---\ $                    *')
                stdscr.addstr(8, 1, '*      $ $ $$           $$ $ $                   *')
                stdscr.addstr(9, 1, '*      $ $$  $         $  $$  $                  *')
                stdscr.addstr(10, 1,'*     $  $ $$           $$ $  $                  *')
                stdscr.addstr(11, 1,'*     $  $                 $  $                  *')
                stdscr.addstr(12, 1,'*    $   $      $$$$$      $   $                 *')
                stdscr.addstr(13, 1,'*    $   $       $$$       $   $                 *')
                stdscr.addstr(14, 1,'*     $  $        $        $  $                  *')
                stdscr.addstr(15, 1,'*      $  $    $  $  $    $  $                   *')
                stdscr.addstr(16, 1,'*       $$ $    $$ $$    $ $$                    *')
                stdscr.addstr(17, 1,'*           $$         $$                        *')
                stdscr.addstr(18, 1,'*             $$$$$$$$$                          *')
                stdscr.addstr(19, 1,'**************************************************')
            if tick_current == 2:
                stdscr.addstr(1, 1, '**************************************************')
                stdscr.addstr(2, 1, '*                   TickBox                      *')
                stdscr.addstr(3, 1, '*                 Tickagotchi                    *')
                stdscr.addstr(4, 1, '**************************************************')
                stdscr.addstr(5, 1, '*          $$$$$$$$$$$$$$$                       *')
                stdscr.addstr(6, 1, '*        $$               $$                     *')
                stdscr.addstr(7, 1, '*       $ ----         ---- $                    *')
                stdscr.addstr(8, 1, '*      $ $ $$           $$ $ $                   *')
                stdscr.addstr(9, 1, '*      $ $$  $         $  $$  $                  *')
                stdscr.addstr(10, 1,'*     $  $ $$           $$ $  $                  *')
                stdscr.addstr(11, 1,'*     $  $                 $  $                  *')
                stdscr.addstr(12, 1,'*    $   $      $$$$$      $   $                 *')
                stdscr.addstr(13, 1,'*    $   $       $$$       $   $                 *')
                stdscr.addstr(14, 1,'*     $  $        $        $  $                  *')
                stdscr.addstr(15, 1,'*      $  $       $       $  $                   *')
                stdscr.addstr(16, 1,'*       $$ $   $$$ $$$   $ $$                    *')
                stdscr.addstr(17, 1,'*           $$         $$                        *')
                stdscr.addstr(18, 1,'*             $$$$$$$$$                          *')
                stdscr.addstr(19, 1,'**************************************************')
            if tick_current == 1:
                stdscr.addstr(1, 1, '**************************************************')
                stdscr.addstr(2, 1, '*                   TickBox                      *')
                stdscr.addstr(3, 1, '*                 Tickagotchi                    *')
                stdscr.addstr(4, 1, '**************************************************')
                stdscr.addstr(5, 1, '*          $$$$$$$$$$$$$$$                       *')
                stdscr.addstr(6, 1, '*        $$               $$                     *')
                stdscr.addstr(7, 1, '*       $ ---\         /--- $                    *')
                stdscr.addstr(8, 1, '*      $ $ $$ \       / $$ $ $                   *')
                stdscr.addstr(9, 1, '*      $ $$  $         $  $$  $                  *')
                stdscr.addstr(10, 1,'*     $  $ $$           $$ $  $                  *')
                stdscr.addstr(11, 1,'*     $  $                 $  $                  *')
                stdscr.addstr(12, 1,'*    $   $      $$$$$      $   $                 *')
                stdscr.addstr(13, 1,'*    $   $       $$$       $   $                 *')
                stdscr.addstr(14, 1,'*     $  $        $        $  $                  *')
                stdscr.addstr(15, 1,'*      $  $     $$$$$     $  $                   *')
                stdscr.addstr(16, 1,'*       $$ $   $     $   $ $$                    *')
                stdscr.addstr(17, 1,'*           $$         $$                        *')
                stdscr.addstr(18, 1,'*             $$$$$$$$$                          *')
                stdscr.addstr(19, 1,'**************************************************')
            if tick_current == 0:
                stdscr.addstr(1, 1, '**************************************************')
                stdscr.addstr(2, 1, '*                   TickBox                      *')
                stdscr.addstr(3, 1, '*                 Tickagotchi                    *')
                stdscr.addstr(4, 1, '**************************************************')
                stdscr.addstr(5, 1, '*          $$$$$$$$$$$$$$$                       *')
                stdscr.addstr(6, 1, '*        $$               $$                     *')
                stdscr.addstr(7, 1, '*       $ ---\         /--- $                    *')
                stdscr.addstr(8, 1, '*      $ $ $$ \       / $$ $ $                   *')
                stdscr.addstr(9, 1, '*      $ $$__$         $__$$  $                  *')
                stdscr.addstr(10, 1,'*     $  $ |            |  $  $                  *')
                stdscr.addstr(11, 1,'*     $  $ |            ^  $  $                  *')
                stdscr.addstr(12, 1,'*    $   $ ^    $$$$$   0  $   $                 *')
                stdscr.addstr(13, 1,'*    $   $ 0     $$$       $   $                 *')
                stdscr.addstr(14, 1,'*     $  $        $        $  $                  *')
                stdscr.addstr(15, 1,'*      $  $     $$$$$     $  $                   *')
                stdscr.addstr(16, 1,'*       $$ $   $_____$   $ $$                    *')
                stdscr.addstr(17, 1,'*           $$         $$                        *')
                stdscr.addstr(18, 1,'*             $$$$$$$$$                          *')
                stdscr.addstr(19, 1,'**************************************************')
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                if tick_current < 4:
                    tick_current += 1
                    start_tick = time.time()
                    tick_timer = start_tick

  	
  	
            stdscr.refresh()   
	
        
        #Debug. Tickagotchi implementation currently accessed by up key for debug. In future, access via web pulse or on box button.
        key = stdscr.getch()
        if key == curses.KEY_UP:
            display_tickagotchi = not display_tickagotchi

        # Refresh the screen
        stdscr.refresh()

def main():
    detect_notifications()
    curses.wrapper(draw_menu)

if __name__ == "__main__":    
    main() 
