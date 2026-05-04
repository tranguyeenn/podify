"""Top-level curses bootstrap for Podify TUI."""

import curses

from podify.ui.input_handlers import handle_key
from podify.ui.router import draw


def main(stdscr):
    # Configure terminal behavior for interactive key-driven UI.
    curses.curs_set(0)
    stdscr.keypad(True)

    # Render + handle input until a handler returns False.
    running = True
    while running:
        draw(stdscr)
        running = handle_key(stdscr.getch())


def run():
    # Wraps setup/teardown so terminal state is restored on exit.
    curses.wrapper(main)
