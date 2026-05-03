import time

from podify.config import sp
from podify.commands import current, get_spotify_volume_percent
from podify.mac_controls import get_mac_output_volume

from podify.ui.constants import DISPLAY_TTL_S

_now_play_cached = ""
_now_play_expiry = 0.0

_vol_line_cached = ""
_vol_line_expiry = 0.0


def invalidate_now_playing_cache():
    global _now_play_expiry
    _now_play_expiry = 0.0


def invalidate_volume_line_cache():
    global _vol_line_expiry
    _vol_line_expiry = 0.0


def get_song():
    try:
        result = current(sp)
        return str(result) if result else "No song playing."
    except Exception as e:
        return f"Spotify error: {e}"


def format_volume_levels() -> str:
    pct = get_spotify_volume_percent(sp)
    if pct is None:
        s_part = "Spotify ?"
    else:
        s_part = f"Spotify {pct}%"

    try:
        m_part = f"Mac {get_mac_output_volume()}%"
    except Exception:
        m_part = "Mac ?"

    return f"{s_part} · {m_part}"


def now_play_line(force=False) -> str:
    global _now_play_cached, _now_play_expiry
    t = time.monotonic()
    if not force and t < _now_play_expiry:
        return _now_play_cached
    try:
        _now_play_cached = get_song()
    except Exception as e:
        _now_play_cached = f"Spotify error: {e}"
    _now_play_expiry = t + DISPLAY_TTL_S
    return _now_play_cached


def volume_meter_line(force=False) -> str:
    global _vol_line_cached, _vol_line_expiry
    t = time.monotonic()
    if not force and t < _vol_line_expiry:
        return _vol_line_cached
    try:
        _vol_line_cached = format_volume_levels()
    except Exception as e:
        _vol_line_cached = f"? · ? ({e})"
    _vol_line_expiry = t + DISPLAY_TTL_S
    return _vol_line_cached
