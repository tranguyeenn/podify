"""Help screen showing core keyboard controls."""

from podify.ui.drawing import frame_outline_row, safe_addstr
from podify.ui.frame import draw_frame
from podify.ui.text_layout import frame_bottom_rule


def draw_help(stdscr):
    # Shared frame shell ensures consistent look with other screens.
    frame = draw_frame(stdscr, "Help")
    if frame == (None, None):
        return

    start_y, start_x = frame

    # Keep this list aligned with key behavior in input_handlers.py.
    lines = [
        "w / up       move up",
        "s / down     move down",
        "enter        select",
        "space        play/pause",
        "a / left     previous",
        "d / right    next",
        "r            refresh queue",
        "m            back/menu",
        "q            quit",
    ]

    ry = start_y + 3
    for ln in lines:
        frame_outline_row(stdscr, ry, start_x, ln)
        ry += 1
    safe_addstr(stdscr, ry, start_x, frame_bottom_rule())
    stdscr.refresh()
