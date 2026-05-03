import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

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
