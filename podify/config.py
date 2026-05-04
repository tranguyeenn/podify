"""Shared Spotify client configuration used by CLI and TUI."""

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load local .env credentials before creating Spotipy client.
load_dotenv()

# App scopes required for playback controls, now-playing reads, and Library screen access.
scope = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing "
    "user-library-read "
    "playlist-read-private "
    "playlist-read-collaborative"
)

# Default Spotipy HTTP timeout is 5s — too aggressive when Wi‑Fi sleeps or Spotify is slow.
_HTTP_TIMEOUT_SEC = 45

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://127.0.0.1:8888/callback",
        requests_timeout=_HTTP_TIMEOUT_SEC,
    ),
    requests_timeout=_HTTP_TIMEOUT_SEC,
    retries=2,
)
