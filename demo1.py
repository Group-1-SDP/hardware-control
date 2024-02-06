import curses
import time
import threading

def scroll_text_line(stdscr, y, x_start, x_end, message, framerate, stop_event):
    pos = x_end  # Starting position of the message (far right)

    # Calculate sleep time based on the frame rate
    sleep_time = 1 / framerate

    while pos > x_start - len(message):
        # Clear the previous message (optional, depending on your requirements)
        stdscr.addstr(y, x_start, ' ' * (x_end - x_start))
        
        # Calculate the position to display the message
        x = pos
        if x + len(message) > x_start and x < x_end:
            # Calculate the substring of the message to display
            if x < x_start:
                display_message = message[-x + x_start:]
                x = x_start
            elif x + len(message) > x_end:
                display_message = message[:x_end - x]
            else:
                display_message = message

            stdscr.addstr(y, x, display_message)  # Add text to the screen buffer

        stdscr.refresh()  # Update the screen
        time.sleep(sleep_time)  # Wait based on frame rate to create the scrolling effect
        pos -= 1  # Move the message to the left

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

def display_time(stdscr, time_in_secs=120):
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

    while True:
        # Convert time_in_secs to minutes and seconds
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
        stdscr.addstr(2, 1,  '*                     Demo 1                        *')
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
        keypress = stdscr.getch()
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

            # threading shit
            stop_event = threading.Event()
            stop_events.append(stop_event)
            # more threading shit
            message_key = chr(keypress)
            new_thread = threading.Thread(target=scroll_text_line, args=(stdscr, 2, 2, width-1, messages[message_key], 20, stop_event))
            threads.append(new_thread)
            new_thread.start()

        time.sleep(1)
        time_in_secs -= 1

def main():
    curses.wrapper(display_time)

if __name__ == "__main__":
    main()