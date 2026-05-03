from podify.ui import state
from podify.ui.constants import FRAME_INNER_W, SEARCH_ROWS
from podify.ui.drawing import frame_outline_row, pick_row_outline, safe_addstr
from podify.ui.frame import draw_frame
from podify.ui.sync import sync_search_scroll
from podify.ui.text_layout import ellip_tw, frame_bottom_rule


def draw_search(stdscr):
    frame = draw_frame(stdscr, "Search")
    if frame == (None, None):
        return

    start_y, start_x = frame
    sync_search_scroll()

    ry = start_y + 3
    q_show = (
        state.search_text
        if state.search_text.strip()
        else ("…" if state.search_pick_mode else "Type query, Enter to search")
    )
    frame_outline_row(stdscr, ry, start_x, q_show)

    ry += 1
    if state.search_pick_mode and state.search_results:
        for i in range(SEARCH_ROWS):
            ix = state.search_scroll + i
            if ix < len(state.search_results):
                tr = state.search_results[ix]
                art = ", ".join(a["name"] for a in tr["artists"])
                lbl = f"{tr['name']} · {art}"
            else:
                lbl = ""

            pick_row_outline(stdscr, ry, start_x, lbl, ix == state.search_pick_ix)
            ry += 1

        footer = ellip_tw("↑↓  Enter plays  Esc query  m home", FRAME_INNER_W)
        frame_outline_row(stdscr, ry, start_x, footer)
        ry += 1
    else:
        frame_outline_row(
            stdscr,
            ry,
            start_x,
            "Enter searches Spotify  bksp clears  Esc cancels picks  m home",
        )
        ry += 1

    safe_addstr(stdscr, ry, start_x, frame_bottom_rule())

    _, wc = stdscr.getmaxyx()
    ry += 2
    safe_addstr(
        stdscr,
        ry,
        start_x,
        ellip_tw(f"Status: {state.status}", max(40, wc - max(2, start_x) - 1)),
    )
    stdscr.refresh()
