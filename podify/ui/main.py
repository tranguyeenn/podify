import curses

from podify.ui.input_handlers import handle_key
from podify.ui.router import draw


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    running = True
    while running:
        draw(stdscr)
        running = handle_key(stdscr.getch())


def run():
    curses.wrapper(main)
