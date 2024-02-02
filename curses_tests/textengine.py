import curses

# Initialize global variables
phone_connected = False
tasks_completed = 0

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Loop where k is the last character pressed
    while k != ord('q'):  # Press 'q' to exit

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == ord('t'):
            global tasks_completed
            tasks_completed += 1

        if k == ord('p'):
            global phone_connected
            phone_connected = not phone_connected

        # Declaration of strings
        title = "Press 'p' to toggle phone connection, 't' to increase tasks, 'q' to exit"[:width-1]
        subtitle = "Enter function: "
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_y = int((height // 2) - 2)

        # Rendering some text
        stdscr.addstr(start_y, start_x_title, title)
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        stdscr.addstr(start_y + 3, (width // 2) - 10, 'Phone connected: [{}]'.format(str(phone_connected)))
        stdscr.addstr(start_y + 4, (width // 2) - 10, '(0/{}) Tasks completed'.format(tasks_completed))

        # Render status bar
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(1))

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
