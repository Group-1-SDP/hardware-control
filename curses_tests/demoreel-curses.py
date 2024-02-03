import curses
import time

def scroll_text(stdscr, framerate):
    # Initialize curses
    curses.curs_set(0)  # Invisible cursor
    stdscr.nodelay(1)  # Don't block I/O calls
    stdscr.timeout(100)  # Wait 100ms for the user to press a key
    height, width = stdscr.getmaxyx()  # Get window dimensions
    message = "Task Complete!"
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

# Initialize curses and set the frame rate
framerate = 24  # Frames per second
curses.wrapper(scroll_text, framerate)
