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

def menu_select(stdscr):
    curses.curs_set(0)  # Hide the cursor
    options = ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
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

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            scroll_text(stdscr, options[current_row])  # Call the animation function
            # Return or break here if you want to exit after selecting an option
            # return or break

def main():
    curses.wrapper(menu_select)

if __name__ == "__main__":
    main()