"""Shared frame and wheel rendering for iPod-style screens."""

import curses

from podify.ui.constants import FRAME_INNER_W, WHEEL_INNER_W
from podify.ui.drawing import safe_addstr
from podify.ui.text_layout import frame_mid_rule, frame_top_rule, inner_center, text_width


def draw_frame(stdscr, title):
    # Clear per frame so each screen draws from a known blank state.
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Hard minimum keeps borders/wheel from clipping.
    if height < 28 or width < 50:
        safe_addstr(stdscr, 1, 2, "Make terminal bigger.")
        safe_addstr(stdscr, 2, 2, f"Current: {width}x{height}")
        safe_addstr(stdscr, 3, 2, "Need: 50x28")
        stdscr.refresh()
        return None, None

    start_y = 1
    fw = FRAME_INNER_W + 2
    start_x = max(2, width // 2 - fw // 2)

    safe_addstr(stdscr, start_y, start_x, frame_top_rule())
    safe_addstr(stdscr, start_y + 1, start_x, "│")
    safe_addstr(stdscr, start_y + 1, start_x + 1, inner_center(title or ""))
    safe_addstr(stdscr, start_y + 1, start_x + 1 + FRAME_INNER_W, "│")
    safe_addstr(stdscr, start_y + 2, start_x, frame_mid_rule())

    return start_y, start_x


def draw_wheel(stdscr, y: int, frame_left_x: int):
    # Draw decorative click-wheel under the content frame.
    wt = WHEEL_INNER_W + 2
    bx = frame_left_x + max(0, (FRAME_INNER_W + 2 - wt) // 2)
    lbl_m = "MENU"
    lbl_s = "SPACE"
    mx = bx + (wt - text_width(lbl_m)) // 2
    sx = bx + (wt - text_width(lbl_s)) // 2

    def row_inner(s: str) -> str:
        g = WHEEL_INNER_W - text_width(s)
        ln = max(0, g // 2)
        rn = max(0, g - ln)
        return (" " * ln) + s + (" " * rn)

    safe_addstr(stdscr, y, mx, lbl_m)
    safe_addstr(stdscr, y + 1, bx, "╭" + ("─" * WHEEL_INNER_W) + "╮")
    safe_addstr(stdscr, y + 2, bx, "│" + row_inner("↑") + "│")
    safe_addstr(stdscr, y + 3, bx, "│" + row_inner("←    ●    →") + "│")
    safe_addstr(stdscr, y + 4, bx, "│" + row_inner("↓") + "│")
    safe_addstr(stdscr, y + 5, bx, "╰" + ("─" * WHEEL_INNER_W) + "╯")
    safe_addstr(stdscr, y + 6, sx, lbl_s)
