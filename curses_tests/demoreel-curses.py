import curses
import time

def scroll_text(stdscr, framerate, message="Task Complete!"):
    # Initialize curses
    curses.curs_set(0)  # Invisible cursor
    stdscr.nodelay(1)  # Don't block I/O calls
    stdscr.timeout(100)  # Wait 100ms for the user to press a key
    height, width = stdscr.getmaxyx()  # Get window dimensions
    pos = width  # Starting position of the message (far right)

    # Calculate sleep time based on the frame rate
    sleep_time = 1 / framerate

    while pos > -len(message):
        stdscr.clear()  # Clear the screen
        # Calculate the position to display the message
        x = pos
        y = height // 2  # Middle of the screen

        # Ensure the text position is within the screen bounds before adding it
        if x + len(message) > 0 and x < width:
            # Calculate the substring of the message to display
            if x < 0:
                display_message = message[-x:]
                x = 0
            elif x + len(message) > width:
                display_message = message[:width - x]
            else:
                display_message = message

            stdscr.addstr(y, x, display_message)  # Add text to the screen buffer

        stdscr.refresh()  # Update the screen
        time.sleep(sleep_time)  # Wait based on frame rate to create the scrolling effect
        pos -= 1  # Move the message to the left

    stdscr.getch()  # Wait for a key press
    curses.endwin()  # Clean up and return terminal to previous state

def add_task(stdscr):
    #k = 0
    # Refresh the screen
    stdscr.refresh()

    # Wait for next input
    #k = stdscr.getch()
    while True: #k!= ord('q'): # Press 'q' to exit
        #Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

           # Render the UI
        stdscr.addstr(1, 1, '**************************************************')
        stdscr.addstr(2, 1, '*                                                *')
        stdscr.addstr(3, 1, '*                                                *')
        stdscr.addstr(4, 1, '*                                                *')
        stdscr.addstr(5, 1, '*                                                *')
        stdscr.addstr(6, 1, '*                                                *')
        stdscr.addstr(7, 1, '*                   :3                           *')
        stdscr.addstr(8, 1, '*                                                *')
        stdscr.addstr(9, 1, '*                                                *')
        stdscr.addstr(10, 1, '*                                               *')
        stdscr.addstr(11, 1, '*                                               *')
        stdscr.addstr(12, 1, '*                                               *')
        stdscr.addstr(13, 1, '*************************************************')

         # Refresh the screen
        stdscr.refresh()

        if stdscr.getch() == ord('q'):
            break

def draw_menu(stdscr):
    phone_connected = False
    dispenser_connected = False
    task_signal = 1
    k = 0

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while k != ord('q'):  # Press 'q' to exit
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Handle input
        if k == ord('p'):
            phone_connected = not phone_connected
        elif k == ord('d'):
            dispenser_connected = not dispenser_connected
        elif ord('0') <= k <= ord('4'):
            task_signal = k - ord('0')
        elif k == ord('z'):
            add_task(stdscr)

        # Render the UI
        stdscr.addstr(1, 1, '**************************************************')
        stdscr.addstr(2, 1, '*                                                *')
        stdscr.addstr(3, 1, '*    Phone connected: [{:<5}]                    *'.format(str(phone_connected)))
        stdscr.addstr(4, 1, '*    Dispenser connected: [{:<5}]                *'.format(str(dispenser_connected)))
        stdscr.addstr(5, 1, '*    Task signal: [{:<2}]                           *'.format(task_signal))
        stdscr.addstr(6, 1, '*                                                *')
        stdscr.addstr(7, 1, '*    "p" toggles phone connection                *')
        stdscr.addstr(8, 1, '*    "d" toggles dispenser connection            *')
        stdscr.addstr(9, 1, '*    Numbers (0-4) change task signal            *')
        stdscr.addstr(10, 1, '*    "s" to sends task pulse                    *')
        stdscr.addstr(11, 1, '*    Press "q" to quit                          *')
        stdscr.addstr(12, 1, '*                                               *')
        stdscr.addstr(13, 1, '*************************************************')

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

        # Send pulse if 's' is pressed
        if k == ord('s'):
            perform_action(stdscr, height, width, phone_connected, dispenser_connected, task_signal)

def perform_action(stdscr, height, width, phone_connected, dispenser_connected, task_signal):
    if phone_connected:
        if not dispenser_connected:
            scroll_text(stdscr, 60, "Task (Level {}) Complete!".format(task_signal))
        else:
            action = 'Jingling' if not dispenser_connected else 'Dispensing'
            message = '{} at strength: {} '.format(action, task_signal)

            # Display the action message
            stdscr.addstr(height - 2, 2, message + " " * (width - len(message) - 3))
            stdscr.refresh()

            # Make the message appear on the UI for only a second
            time.sleep(1)

            # Clear the message
            stdscr.addstr(height - 2, 2, " " * (width - 3))
            stdscr.refresh()

def play_video(stdscr, framerate, frames_file='DemoVideoFrames.txt'):
    # Set getch to non-blocking
    stdscr.nodelay(True)

    # Read the frames from the file
    with open(frames_file, 'r') as file:
        content = file.read()

    # Split the content by the unique delimiter to get each frame
    frames = content.split('<--frame-->\n')[:-1]  # The last split is empty

    # Calculate sleep time based on the frame rate
    sleep_time = 1 / framerate

    # Get the size of the terminal window and adjust to avoid the edges
    height, width = stdscr.getmaxyx()
    height -= 1
    width -= 1
    
    for frame in frames:
        stdscr.clear()  # Clear the screen

        # Split the frame into lines
        lines = frame.split('\n')

        # Display each line in the frame, making sure not to exceed the screen's boundaries
        for i, line in enumerate(lines):
            if i < height - 1:  # Avoid writing to the last line
                # Truncate line to fit screen's width and avoid the last column
                stdscr.addstr(i, 0, line[:width - 1])

        # If the user presses 'q', exit the video
        if stdscr.getch() == ord('q'):
            break
        stdscr.refresh()  # Refresh the screen
        time.sleep(sleep_time)  # Wait for the frame duration

    stdscr.getch()
    curses.endwin()

def menu_select(stdscr):
    curses.curs_set(0)  # Hide the cursor
    options = ["Simple 'Task Complete'", "Basic Menu", "Video Playback ([q] to end)", "Not implemented", "Quit"]
    current_row = 0

    while True:
        stdscr.clear()

        h, w = stdscr.getmaxyx()  # Get the window's height and width

        for idx, option in enumerate(options):
            x = w//2 - len(option)//2
            y = h//2 - len(options)//2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, option)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, option)

        stdscr.refresh()

        key = stdscr.getch()

        # Menu nav handling
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        # Selection handling
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                scroll_text(stdscr, 30)
            elif current_row == 1:
                draw_menu(stdscr)
            elif current_row == 2:
                play_video(stdscr, 30)
            elif current_row == 4:
                break

def main():
    curses.wrapper(menu_select)

if __name__ == "__main__":
    main()