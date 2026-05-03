from podify.config import sp
from podify.commands import QUEUE_PREVIEW_MAX, upcoming_queue_lines

from podify.ui import state
from podify.ui.constants import QUEUE_VISIBLE_ROWS, SEARCH_ROWS


def sync_search_scroll():
    if not state.search_results:
        state.search_scroll = 0
        return
    state.search_pick_ix = max(0, min(state.search_pick_ix, len(state.search_results) - 1))
    v = SEARCH_ROWS
    if state.search_pick_ix < state.search_scroll:
        state.search_scroll = state.search_pick_ix
    if state.search_pick_ix >= state.search_scroll + v:
        state.search_scroll = state.search_pick_ix - v + 1
    max_scr = max(0, len(state.search_results) - v)
    state.search_scroll = max(0, min(state.search_scroll, max_scr))


def reset_search_pick():
    state.search_results = []
    state.search_pick_ix = 0
    state.search_scroll = 0
    state.search_pick_mode = False


def sync_queue_scroll():
    n = len(state.queue_rows)
    if n <= 0:
        state.queue_scroll = 0
        return
    max_scr = max(0, n - QUEUE_VISIBLE_ROWS)
    state.queue_scroll = max(0, min(state.queue_scroll, max_scr))


def load_queue_preview():
    rows, err = upcoming_queue_lines(sp, limit=QUEUE_PREVIEW_MAX)
    state.queue_error = err or ""
    state.queue_rows = rows if not err else []
    state.queue_scroll = 0
    sync_queue_scroll()
