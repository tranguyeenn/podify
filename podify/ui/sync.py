"""State synchronization helpers for scroll windows and refreshes."""

from podify.config import sp
from podify.commands import (
    QUEUE_PREVIEW_MAX,
    playlist_tracks,
    upcoming_queue_lines,
    user_library_playlists,
)

from podify.ui import state
from podify.ui.constants import LIBRARY_ROWS, QUEUE_VISIBLE_ROWS


def sync_library_scroll():
    # Empty library means no valid cursor/scroll.
    if not state.library_rows:
        state.library_scroll = 0
        return
    # Clamp highlighted row to current data bounds.
    state.library_pick_ix = max(0, min(state.library_pick_ix, len(state.library_rows) - 1))
    # Visible row window size.
    v = LIBRARY_ROWS
    # Keep cursor above top edge.
    if state.library_pick_ix < state.library_scroll:
        state.library_scroll = state.library_pick_ix
    # Keep cursor below bottom edge.
    if state.library_pick_ix >= state.library_scroll + v:
        state.library_scroll = state.library_pick_ix - v + 1
    # Clamp scroll to max possible range.
    max_scr = max(0, len(state.library_rows) - v)
    state.library_scroll = max(0, min(state.library_scroll, max_scr))


def load_library_preview():
    # Library root lists all playlists so user can drill into tracks.
    state.library_mode = "playlists"
    state.library_playlist_id = ""
    state.library_playlist_name = ""
    state.library_rows = user_library_playlists(sp, limit=50)
    # Start at first row after each refresh.
    state.library_pick_ix = 0
    state.library_scroll = 0
    # Final clamp in case response is empty.
    sync_library_scroll()


def load_library_playlist_tracks(playlist_id: str, playlist_name: str):
    # Switch Library into track mode for the selected playlist.
    state.library_mode = "tracks"
    state.library_playlist_id = str(playlist_id or "")
    state.library_playlist_name = str(playlist_name or "")
    state.library_rows = playlist_tracks(sp, state.library_playlist_id, limit=100)
    state.library_pick_ix = 0
    state.library_scroll = 0
    sync_library_scroll()


def sync_queue_scroll():
    # Normalize queue scroll after refresh/navigation.
    n = len(state.queue_rows)
    if n <= 0:
        state.queue_scroll = 0
        return
    # Clamp queue scroll to valid viewport range.
    max_scr = max(0, n - QUEUE_VISIBLE_ROWS)
    state.queue_scroll = max(0, min(state.queue_scroll, max_scr))


def load_queue_preview():
    # Pull queue snapshot and normalize view state.
    rows, err = upcoming_queue_lines(sp, limit=QUEUE_PREVIEW_MAX)
    state.queue_error = err or ""
    state.queue_rows = rows if not err else []
    state.queue_scroll = 0
    sync_queue_scroll()
