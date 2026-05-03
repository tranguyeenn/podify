from podify.ui import state
from podify.ui.drawing import frame_outline_row, safe_addstr
from podify.ui.frame import draw_frame
from podify.ui.readouts import volume_meter_line
from podify.ui.text_layout import ellip_tw, frame_bottom_rule


def draw_volume(stdscr):
    frame = draw_frame(stdscr, "Volume")
    if frame == (None, None):
        return

    start_y, start_x = frame

    frame_outline_row(stdscr, start_y + 3, start_x, "Type volume 0-100:")
    frame_outline_row(stdscr, start_y + 4, start_x, state.volume_text or "")
    frame_outline_row(stdscr, start_y + 5, start_x, volume_meter_line(force=False))
    frame_outline_row(stdscr, start_y + 6, start_x, "Enter: Set Spotify volume")
    frame_outline_row(stdscr, start_y + 7, start_x, "+ / = louder  - quieter (Mac)")
    frame_outline_row(stdscr, start_y + 8, start_x, "M: Back")

    safe_addstr(stdscr, start_y + 9, start_x, frame_bottom_rule())
    _, wc = stdscr.getmaxyx()
    safe_addstr(
        stdscr,
        start_y + 11,
        start_x,
        ellip_tw(f"Status: {state.status}", max(40, wc - max(2, start_x) - 1)),
    )
    stdscr.refresh()
