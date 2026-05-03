import curses

from podify.ui.constants import FRAME_INNER_W
from podify.ui import state
from podify.ui.drawing import safe_addstr
from podify.ui.frame import draw_frame, draw_wheel
from podify.ui.text_layout import ellip_tw, frame_bottom_rule, pad_to_width, text_width


def draw_menu(stdscr, title, items):
    frame = draw_frame(stdscr, title)
    if frame == (None, None):
        return

    start_y, start_x = frame

    for i, item in enumerate(items):
        y = start_y + 3 + i
        sel2 = "> " if i == state.selected else "  "
        rhs = ">"
        mid = FRAME_INNER_W - text_width(sel2) - text_width(rhs)
        lab = pad_to_width(ellip_tw(str(item), mid), mid)
        inner = sel2 + lab + rhs
        safe_addstr(stdscr, y, start_x, "│")
        safe_addstr(
            stdscr,
            y,
            start_x + 1,
            inner,
            curses.A_REVERSE if i == state.selected else 0,
        )
        safe_addstr(stdscr, y, start_x + 1 + FRAME_INNER_W, "│")

    bottom = start_y + 3 + len(items)
    safe_addstr(stdscr, bottom, start_x, frame_bottom_rule())
    safe_addstr(stdscr, bottom + 2, start_x, f"Status: {state.status[:30]}")
    draw_wheel(stdscr, bottom + 4, start_x)
    safe_addstr(stdscr, bottom + 12, start_x, "w/s = move | enter = select | m = back | q = quit")

    stdscr.refresh()
