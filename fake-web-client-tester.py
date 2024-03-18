from flask import Flask, request, jsonify
from flask_socketio import SocketIO
import curses

def client(stdscr):
    app = Flask(__name__)
    sio = SocketIO(app, cors_allowed_origins="*")
    curses.noecho()

    while True:
        stdscr.clear()

        stdscr.addstr(1, 1, '**************************************************')
        stdscr.addstr(2, 1, '*                   TickBox                      *')
        stdscr.addstr(3, 1, '*                Fake web client                 *')
        stdscr.addstr(4, 1, '**************************************************')
        stdscr.addstr(5, 1, '*                                                *')
        stdscr.addstr(6, 1, '*                                                *')
        stdscr.addstr(7, 1, '*             Press UP to complete               *')
        stdscr.addstr(8, 1, '*                     task                       *')
        stdscr.addstr(9, 1, '*                                                *')
        stdscr.addstr(10, 1,'*                                                *')
        stdscr.addstr(11, 1,'*                                                *')
        stdscr.addstr(12, 1,'*                                                *')
        stdscr.addstr(13, 1,'*                                                *')
        stdscr.addstr(14, 1,'*                                                *')
        stdscr.addstr(15, 1,'*                                                *')
        stdscr.addstr(16, 1,'*                                                *')
        stdscr.addstr(17, 1,'*                                                *')
        stdscr.addstr(18, 1,'*                                                *')
        stdscr.addstr(19, 1,'**************************************************')

        key = stdscr.getch()
        if key == curses.KEY_UP:
            sio.emit('task-complete')
        stdscr.refresh()

def main(): 
    curses.wrapper(client)

if __name__ == "__main__":    
    main()  
