"""Library screen showing saved Spotify tracks with a picker."""

from podify.ui import state
from podify.ui.constants import FRAME_INNER_W, LIBRARY_ROWS
from podify.ui.drawing import frame_outline_row, pick_row_outline, safe_addstr
from podify.ui.frame import draw_frame
from podify.ui.sync import sync_library_scroll
from podify.ui.text_layout import ellip_tw, frame_bottom_rule


def draw_library(stdscr):
    # Reuse shared frame style so Library feels like other screens.
    frame = draw_frame(stdscr, "Library")
    if frame == (None, None):
        return

    start_y, start_x = frame
    # Ensure cursor/scroll are valid before drawing rows.
    sync_library_scroll()

    # Header reflects current drill-down level.
    head = (
        "Playlists (Spotify) · Enter opens · Esc back"
        if state.library_mode == "playlists"
        else f"{state.library_playlist_name or 'Playlist'} · Enter plays · Esc playlists"
    )
    frame_outline_row(stdscr, start_y + 3, start_x, head)
    ry = start_y + 4

    # Render empty-state for either playlist level or track level.
    if not state.library_rows:
        msg = (
            "No playlists found."
            if state.library_mode == "playlists"
            else "No tracks found in this playlist."
        )
        frame_outline_row(stdscr, ry, start_x, msg)
        ry += 1
    else:
        # Draw a fixed-size viewport; scroll picks which rows are visible.
        for i in range(LIBRARY_ROWS):
            ix = state.library_scroll + i
            if ix < len(state.library_rows):
                row = state.library_rows[ix]
                if state.library_mode == "playlists":
                    # Playlist rows show title and track count.
                    total = ((row.get("tracks") or {}).get("total")) or 0
                    owner = ((row.get("owner") or {}).get("display_name")) or "?"
                    lbl = f"{row.get('name', '?')} · {total} tracks · {owner}"
                else:
                    # Track rows show song + artists.
                    art = ", ".join(a["name"] for a in row.get("artists", []) if a.get("name"))
                    lbl = f"{row.get('name', '?')} · {art or '?'}"
            else:
                lbl = ""
            pick_row_outline(stdscr, ry, start_x, lbl, ix == state.library_pick_ix)
            ry += 1

    # Footer shows row window if data exists, else simple back hint.
    foot = (
        f"↑↓ rows {state.library_scroll + 1}-"
        f"{min(state.library_scroll + LIBRARY_ROWS, len(state.library_rows))}/{len(state.library_rows)} · m"
        if state.library_rows
        else "m menu"
    )
    frame_outline_row(stdscr, ry, start_x, ellip_tw(foot, FRAME_INNER_W))
    ry += 1
    safe_addstr(stdscr, ry, start_x, frame_bottom_rule())

    # Shared status line near frame bottom.
    _, wc = stdscr.getmaxyx()
    safe_addstr(
        stdscr,
        ry + 2,
        start_x,
        ellip_tw(f"Status: {state.status}", max(40, wc - max(2, start_x) - 1)),
    )
    stdscr.refresh()
