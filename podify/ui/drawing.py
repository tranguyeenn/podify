"""Low-level safe drawing primitives for curses screens."""

import curses

from podify.ui.constants import FRAME_INNER_W
from podify.ui.text_layout import ellip_tw, inner_left, pad_to_width, text_width


def safe_addstr(stdscr, y, x, text, attr=0):
    # Guard against out-of-bounds writes on small terminal sizes.
    height, width = stdscr.getmaxyx()

    if y < 0 or y >= height or x < 0 or x >= width:
        return

    # Truncate to visible width so curses doesn't throw.
    text = str(text)[: max(0, width - x - 1)]

    try:
        stdscr.addstr(y, x, text, attr)
    except curses.error:
        pass


def frame_outline_row(stdscr, y: int, start_x: int, inner_plain: str, attr=0):
    # Draw one full frame row with left/right borders.
    inner = inner_left(inner_plain)
    safe_addstr(stdscr, y, start_x, "│")
    safe_addstr(stdscr, y, start_x + 1, inner, attr)
    safe_addstr(stdscr, y, start_x + 1 + FRAME_INNER_W, "│")


def pick_row_outline(stdscr, y: int, start_x: int, label_plain: str, is_sel: bool):
    # Draw selectable row with pointer and highlighted state.
    sel2 = "> " if is_sel else "  "
    rhs = ">"
    mid = FRAME_INNER_W - text_width(sel2) - text_width(rhs)
    lab = pad_to_width(ellip_tw(label_plain, mid), mid)
    inner = sel2 + lab + rhs
    safe_addstr(stdscr, y, start_x, "│")
    safe_addstr(stdscr, y, start_x + 1, inner, curses.A_REVERSE if is_sel else 0)
    safe_addstr(stdscr, y, start_x + 1 + FRAME_INNER_W, "│")
