"""Mutable UI state shared across draw and input modules."""

# Active screen key; router draws by this value.
screen = "main"
# Current highlighted item index for menu-like screens.
selected = 0
# Bottom-line status text shown in multiple screens.
status = "Welcome to Podify"
# Text buffer for volume input screen.
volume_text = ""

# Library screen state (saved tracks + highlighted row).
# Current Library mode: "playlists" first, then "tracks".
library_mode = "playlists"
# Selected playlist metadata used when viewing its tracks.
library_playlist_id = ""
library_playlist_name = ""
# Rows for current library mode (playlist dicts or track dicts).
library_rows: list[dict] = []
# Highlighted row inside current library_rows window.
library_pick_ix = 0
# Scroll offset for library list virtualization.
library_scroll = 0

# Render-ready queue lines for queue screen.
queue_rows: list[str] = []
# Scroll offset for queue viewport.
queue_scroll = 0
# Last queue refresh error text (empty when healthy).
queue_error = ""
