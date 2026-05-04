"""Queue preview screen with refresh and scrolling."""

from podify.commands import QUEUE_PREVIEW_MAX

from podify.ui import state
from podify.ui.constants import FRAME_INNER_W, QUEUE_VISIBLE_ROWS
from podify.ui.drawing import frame_outline_row, safe_addstr
from podify.ui.frame import draw_frame
from podify.ui.sync import sync_queue_scroll
from podify.ui.text_layout import ellip_tw, frame_bottom_rule


def draw_queue(stdscr):
    # Draw frame shell and normalize scroll before rendering rows.
    frame = draw_frame(stdscr, "Queue")
    if frame == (None, None):
        return

    start_y, start_x = frame
    sync_queue_scroll()

    head = f"Up next (up to {QUEUE_PREVIEW_MAX}) · r refresh"
    frame_outline_row(stdscr, start_y + 3, start_x, head)
    ry = start_y + 4

    # Body supports error, empty, and filled queue states.
    if state.queue_error:
        frame_outline_row(stdscr, ry, start_x, ellip_tw(state.queue_error, FRAME_INNER_W))
        ry += 1
    elif not state.queue_rows:
        frame_outline_row(stdscr, ry, start_x, "Empty (or Spotify returned none).")
        ry += 1
    else:
        for i in range(QUEUE_VISIBLE_ROWS):
            ix = state.queue_scroll + i
            if ix < len(state.queue_rows):
                frame_outline_row(stdscr, ry, start_x, state.queue_rows[ix])
            else:
                frame_outline_row(stdscr, ry, start_x, "")
            ry += 1

    # Footer switches between row-range status and simple controls.
    if state.queue_rows and len(state.queue_rows) > QUEUE_VISIBLE_ROWS:
        lo = state.queue_scroll + 1
        hi = min(state.queue_scroll + QUEUE_VISIBLE_ROWS, len(state.queue_rows))
        foot = f"↑↓ rows {lo}-{hi}/{len(state.queue_rows)} · r · m"
    else:
        foot = "w/s scroll · r refresh · m menu"
    frame_outline_row(stdscr, ry, start_x, ellip_tw(foot, FRAME_INNER_W))
    ry += 1
    safe_addstr(stdscr, ry, start_x, frame_bottom_rule())
    _, wc = stdscr.getmaxyx()
    safe_addstr(
        stdscr,
        ry + 2,
        start_x,
        ellip_tw(f"Status: {state.status}", max(40, wc - max(2, start_x) - 1)),
    )
    stdscr.refresh()
