"""Spotify command helpers shared by CLI and TUI flows."""

from spotipy.exceptions import SpotifyException
from colorama import Fore, Style

def current(sp):
    # Return compact "track - artists" string for current playback.
    current_track = sp.current_user_playing_track()

    if current_track is not None and current_track["item"] is not None:
        track_name = current_track["item"]["name"]
        artists = ", ".join(
            artist["name"] for artist in current_track["item"]["artists"]
        )

        return f"{track_name} - {artists}"

    return "No track is currently playing."

def pause(sp):
    # Pause active Spotify playback.
    sp.pause_playback()
    print("⏸ paused.")

def next_track(sp):
    # Skip to next track in current playback context.
    sp.next_track()
    print("⏭ skipped.")

def previous(sp):
    # Previous track can be blocked by Spotify in some contexts.
    try:
        sp.previous_track()
        print("⏮ previous track")
    except SpotifyException as e:
        if e.http_status == 403:
            print()
            print(Fore.RED + "Spotify blocked previous track for this playback.")
            print(Fore.RED + "Try playing from a normal playlist/album, not queue/radio/podcast/ad.")
        else:
            print(Fore.RED + f"Spotify error: {e}")

def play(sp):
    # Resume playback on active Spotify device/context.
    try:
        sp.start_playback()
        print("▶️  Playback started.")
    except SpotifyException as e:
        print(Fore.RED + f"Spotify error: {e}")

def get_spotify_volume_percent(sp):
    """Device volume from active playback, or None if unknown."""
    try:
        pb = sp.current_playback()
        if not pb:
            return None
        dev = pb.get("device") or {}
        v = dev.get("volume_percent")
        if v is None:
            return None
        return int(v)
    except Exception:
        return None


def handle_volume(sp, args):
    # CLI parser for `volume <0-100>`.
    if len(args) != 1:
        print("Usage: volume <0-100>")
        return

    try:
        vol = int(args[0])

        if vol < 0 or vol > 100:
            print("Volume must be between 0 and 100.")
            return

        sp.volume(vol)
        print(f"Spotify volume set to {vol}%")

    except ValueError:
        print("Volume must be a number.")
    except Exception:
        print("Failed to set Spotify volume. Is Spotify active?")

def saved_library_tracks(sp, limit: int = 50):
    """Fetch the user's saved tracks from Spotify's library endpoint."""
    # Spotify caps this endpoint at 50 per request.
    cap = min(max(1, int(limit)), 50)
    resp = sp.current_user_saved_tracks(limit=cap, offset=0)
    rows = []
    for item in (resp or {}).get("items", []):
        # Endpoint wraps each row as {added_at, track}.
        tr = (item or {}).get("track")
        # Only keep playable tracks with a URI.
        if isinstance(tr, dict) and tr.get("uri"):
            rows.append(tr)
    return rows


def user_library_playlists(sp, limit: int = 50):
    """Fetch the user's playlists for Library playlist-first navigation."""
    # Includes public/private/collab playlists when scopes allow it.
    cap = min(max(1, int(limit)), 50)
    resp = sp.current_user_playlists(limit=cap, offset=0)
    rows = []
    for item in (resp or {}).get("items", []):
        if not isinstance(item, dict):
            continue
        if not item.get("id"):
            continue
        rows.append(item)
    return rows


def playlist_tracks(sp, playlist_id: str, limit: int = 50):
    """Fetch playable tracks from a playlist."""
    if not playlist_id:
        return []
    cap = min(max(1, int(limit)), 100)
    resp = sp.playlist_items(
        playlist_id,
        limit=cap,
        offset=0,
        additional_types=("track",),
    )
    rows = []
    for item in (resp or {}).get("items", []):
        tr = (item or {}).get("track")
        # Keep only tracks with a URI so Enter can play reliably.
        if isinstance(tr, dict) and tr.get("uri"):
            rows.append(tr)
    return rows


QUEUE_PREVIEW_MAX = 30


def _format_queue_track_or_episode(item: dict) -> str:
    if not isinstance(item, dict):
        return "?"
    name = item.get("name") or "?"
    artists = item.get("artists")
    if isinstance(artists, list) and artists:
        parts = []
        for a in artists:
            if isinstance(a, dict) and (nm := (a.get("name") or "").strip()):
                parts.append(nm)
        if parts:
            return f"{name} · {', '.join(parts)}"
    show = item.get("show")
    if isinstance(show, dict) and show.get("name"):
        return f"{name} · {show['name']}"
    return name


def upcoming_queue_lines(sp, limit: int = QUEUE_PREVIEW_MAX):
    """Upcoming titles from Spotify's player queue (~GET /me/player/queue).

    The API omits hidden tail and may cap below ``limit``. The first queue entry
    is sometimes a duplicate of ``currently_playing``; we skip one such dup.
    """
    cap = max(1, min(QUEUE_PREVIEW_MAX, int(limit)))

    try:
        resp = sp.queue()
    except Exception as e:
        return [], str(e)

    if not isinstance(resp, dict):
        return [], None

    cur_uri = ""
    cur = resp.get("currently_playing")
    if isinstance(cur, dict):
        cur_uri = cur.get("uri") or ""

    raw = list(resp.get("queue") or [])
    lines_out: list[str] = []
    skipped_cur_dup = False

    for it in raw:
        if len(lines_out) >= cap:
            break
        if not isinstance(it, dict):
            continue
        u = it.get("uri") or ""
        if cur_uri and u == cur_uri and not skipped_cur_dup:
            skipped_cur_dup = True
            continue

        label = _format_queue_track_or_episode(it)
        n = len(lines_out) + 1
        lines_out.append(f"{n}. {label}")

    return lines_out, None


# Fallback list when album context playback is not possible: keep small → fast POST, fewer timeouts.
FALLBACK_QUEUE_CAP = 50


def _playback_device_id(sp) -> str | None:
    """Active Spotify Connect device id, if API exposes one (helps context/uris queues land correctly)."""
    try:
        pb = sp.current_playback()
        if pb:
            dev = pb.get("device") or {}
            did = dev.get("id")
            if did:
                return str(did)
    except Exception:
        pass
    try:
        for d in (sp.devices().get("devices") or []):
            if d.get("is_active") and d.get("id"):
                return str(d["id"])
    except Exception:
        pass
    return None


def _start_playback(sp, *, device_id: str | None, **kwargs) -> None:
    if device_id:
        sp.start_playback(device_id=device_id, **kwargs)
    else:
        sp.start_playback(**kwargs)


def play_playlist_track_in_order(sp, playlist_id: str, track_uri: str, track_payload=None):
    """Start playlist context at the chosen track so queue stays in playlist order."""
    if not track_uri:
        return
    pid = str(playlist_id or "").strip()
    if not pid:
        # Without a playlist context, fall back to generic single-track playback.
        play_track_uri(sp, track_uri, track_payload)
        return

    dev = _playback_device_id(sp)
    p_uri = pid if pid.startswith("spotify:playlist:") else f"spotify:playlist:{pid}"
    try:
        # Force deterministic playlist order (iPod behavior) before context start.
        try:
            if dev:
                sp.shuffle(False, device_id=dev)
            else:
                sp.shuffle(False)
        except Exception:
            # Ignore pre-toggle failures; we'll retry after playback starts.
            pass

        # Context playback preserves playlist sequence from the selected offset.
        _start_playback(sp, device_id=dev, context_uri=p_uri, offset={"uri": track_uri})
        # Some Spotify clients flip shuffle on context switch; force OFF again.
        try:
            dev2 = _playback_device_id(sp)
            if dev2:
                sp.shuffle(False, device_id=dev2)
            else:
                sp.shuffle(False)
        except Exception:
            pass
    except Exception:
        # Fallback keeps playback resilient if context start fails.
        play_track_uri(sp, track_uri, track_payload)


def _search_tracks_many(sp, q: str, limit: int = 40, offset: int = 0):
    try:
        r = sp.search(
            q=q,
            type="track",
            limit=min(max(1, limit), 50),
            offset=min(max(0, offset), 950),
        )
        return (r.get("tracks") or {}).get("items") or []
    except Exception:
        return []


def _push_unique(bucket: list, seen: set, uris_iter, cap: int):
    for u in uris_iter:
        if not u or u in seen:
            continue
        if len(bucket) >= cap:
            break
        seen.add(u)
        bucket.append(u)


def _album_suffix_one_fetch(sp, album_id: str, track_uri: str, tid: str | None, max_tail: int) -> list[str]:
    """One ``album_tracks`` request (limit 50); skips if album only has one track."""
    try:
        page = sp.album_tracks(album_id, limit=50, offset=0)
        if int(page.get("total") or 0) <= 1:
            return []
    except Exception:
        return []

    seq = [(it.get("uri") or "") for it in (page.get("items") or []) if it.get("uri")]
    ts = str(tid) if tid else ""
    idx = -1
    for i, u in enumerate(seq):
        if u == track_uri or (ts and u.endswith(ts)):
            idx = i
            break

    if idx < 0:
        return []

    return seq[idx : idx + max_tail]


def _compose_queue_lite(sp, uri: str, tp: dict) -> list[str]:
    """Minimal reads: picked track → album continuation (≤1 catalog request) → one artist search."""
    tid = tp.get("id") or ""
    if not tid and ":" in uri:
        ps = uri.split(":")
        if len(ps) >= 3 and ps[-2] == "track":
            tid = ps[-1]

    album_id = (tp.get("album") or {}).get("id")
    first = (tp.get("artists") or [{}])[0]
    artist_name = (first.get("name") or "").replace('"', "").strip()

    bucket: list[str] = []
    seen: set[str] = set()
    cap = FALLBACK_QUEUE_CAP

    _push_unique(bucket, seen, [uri], cap)

    if album_id:
        tail = _album_suffix_one_fetch(sp, album_id, uri, tid, max_tail=38)
        _push_unique(bucket, seen, tail, cap)

    if artist_name and len(bucket) < cap:
        items = _search_tracks_many(
            sp, f'artist:"{artist_name}"', limit=min(40, cap - len(bucket) + 5), offset=0
        )
        _push_unique(bucket, seen, (t.get("uri") for t in items if t.get("uri")), cap)

    return bucket[:cap]


def play_track_uri(sp, uri: str, track_payload=None):
    """Prefer album context (1 quick play). Otherwise a short capped queue built with minimal API chatter."""
    if not uri:
        return

    dev = _playback_device_id(sp)
    tp = track_payload if isinstance(track_payload, dict) else {}
    alb = tp.get("album") or {}
    aid, auri = alb.get("id"), alb.get("uri")

    # Fast lane: Spotify app handles “what’s next” for the LP (minimal requests).
    if aid and auri:
        try:
            h = sp.album_tracks(aid, limit=1)
            if int(h.get("total") or 0) > 1:
                try:
                    _start_playback(
                        sp, device_id=dev, context_uri=auri, offset={"uri": uri}
                    )
                    return
                except Exception:
                    pass
        except Exception:
            pass

    try:
        q = _compose_queue_lite(sp, uri, tp)
        uris = (q if q else [uri])[:FALLBACK_QUEUE_CAP]
        _start_playback(sp, device_id=dev, uris=uris)
    except Exception:
        try:
            _start_playback(sp, device_id=dev, uris=[uri])
        except Exception:
            pass


def handle_search(sp, args):
    """CLI entry: numbered pick via stdin (TTY)."""
    if not args:
        print("Usage: search <song name>")
        return
    # CLI keeps free-text search for terminal-only workflows.
    query = " ".join(args)

    try:
        # Use Spotipy's native search API directly (no local wrapper).
        resp = sp.search(q=query, type="track", limit=10)
        tracks = (resp.get("tracks") or {}).get("items") or []

        if not tracks:
            print("No results found.")
            return

        print("\nSearch results:")
        for i, track in enumerate(tracks, start=1):
            artists = ", ".join(artist["name"] for artist in track["artists"])
            print(f"{i}. {track['name']} by {artists}")

        choice = input("Enter the number of the track to play (or 'cancel'): ").strip()
        if not choice or choice.lower() == "cancel":
            return
        # Convert 1-based user choice to 0-based index.
        index = int(choice) - 1
        if index < 0 or index >= len(tracks):
            print("Invalid choice.")
            return

        play_track_uri(sp, tracks[index]["uri"], tracks[index])
        print("▶️ Playing (album context if possible; else short artist queue).")

    except Exception as e:
        print(Fore.RED + f"Search failed: {e}")
        