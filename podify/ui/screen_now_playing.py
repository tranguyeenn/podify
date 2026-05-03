from podify.ui.drawing import frame_outline_row, safe_addstr
from podify.ui.frame import draw_frame, draw_wheel
from podify.ui.readouts import now_play_line
from podify.ui.text_layout import frame_bottom_rule


def draw_now_playing(stdscr):
    frame = draw_frame(stdscr, "Now Playing")
    if frame == (None, None):
        return

    start_y, start_x = frame
    song = now_play_line(force=False)

    frame_outline_row(stdscr, start_y + 3, start_x, "Track:")
    frame_outline_row(stdscr, start_y + 4, start_x, song or "")
    frame_outline_row(stdscr, start_y + 5, start_x, "")
    frame_outline_row(stdscr, start_y + 6, start_x, "Space: Play/Pause")
    frame_outline_row(stdscr, start_y + 7, start_x, "Left: Previous    Right: Next")
    frame_outline_row(stdscr, start_y + 8, start_x, "M: Back")

    safe_addstr(stdscr, start_y + 9, start_x, frame_bottom_rule())
    draw_wheel(stdscr, start_y + 11, start_x)
    stdscr.refresh()
