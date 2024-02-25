import curses
import requests
from nfc import NfcReader

def draw_menu(stdscr):
    phone_connected = False
    dispenser_connected = False
    task_signal = 1
    k = 0
    url="http://172.21.12.173:5000/websocket/"

    stdscr.nodelay(1)

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

        # Handle input

        if nfcReader.get_reading():
            phone_connected = True
            requests.post(url + "phoneConnected")
        else:
            phone_connected = False
            requests.post(url + "phoneDisconnected")
        #if k == ord('p'):
        #    phone_connected = not phone_connected
        if k == ord('d'):
            dispenser_connected = not dispenser_connected
        elif ord('0') <= k <= ord('4'):
            task_signal = k - ord('0')
        elif k == ord('z'):
            task = add_task(stdscr)
            tasks.append(task)

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
