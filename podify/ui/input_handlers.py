"""Keyboard input dispatcher for all TUI screens."""

import curses

from podify.config import sp
from podify.commands import next_track, pause, play_playlist_track_in_order, previous
from podify.mac_controls import nudge_mac_volume

from podify.ui import state
from podify.ui.constants import main_menu, playback_menu
from podify.ui.navigation import go_back, select_main, select_playback
from podify.ui.readouts import (
    invalidate_now_playing_cache,
    invalidate_volume_line_cache,
    now_play_line,
    volume_meter_line,
)
from podify.ui.constants import QUEUE_VISIBLE_ROWS
from podify.ui.sync import (
    load_library_playlist_tracks,
    load_library_preview,
    load_queue_preview,
    sync_library_scroll,
)
from podify.ui.text_layout import ellip_tw


def handle_key(key) -> bool:
    # For menu-like screens, decide which item list navigation should use.
    current_items = main_menu if state.screen == "main" else playback_menu

    # Global quit hotkey.
    if key == ord("q"):
        return False

    # Global "menu/home" hotkey.
    if key == ord("m"):
        go_back()
        return True

    if state.screen in ["main", "playback"]:
        # Shared up/down menu movement.
        if key in [ord("w"), curses.KEY_UP]:
            state.selected = (state.selected - 1) % len(current_items)

        elif key in [ord("s"), curses.KEY_DOWN]:
            state.selected = (state.selected + 1) % len(current_items)

        elif key in [10, 13]:
            # Enter dispatches to the current screen selector.
            if state.screen == "main":
                return select_main()
            return select_playback()

    elif state.screen == "now":
        # Space toggles pause from the Now Playing screen.
        if key == ord(" "):
            try:
                pause(sp)
                invalidate_now_playing_cache()
                state.status = "Paused"
            except Exception as e:
                state.status = f"Error: {e}"

        elif key in [ord("a"), curses.KEY_LEFT]:
            # Left = previous track.
            try:
                previous(sp)
                invalidate_now_playing_cache()
                state.status = now_play_line(force=True)
            except Exception as e:
                state.status = f"Error: {e}"

        elif key in [ord("d"), curses.KEY_RIGHT]:
            # Right = next track.
            try:
                next_track(sp)
                invalidate_now_playing_cache()
                state.status = now_play_line(force=True)
            except Exception as e:
                state.status = f"Error: {e}"

    elif state.screen == "library":
        # Library flow: playlists -> tracks -> play.
        if key in (curses.KEY_UP, ord("w")) and state.library_rows:
            # Wrap around when moving above first item.
            state.library_pick_ix = (
                state.library_pick_ix - 1 if state.library_pick_ix else len(state.library_rows) - 1
            )
            sync_library_scroll()
        elif key in (curses.KEY_DOWN, ord("s")) and state.library_rows:
            # Wrap around when moving below last item.
            state.library_pick_ix = (state.library_pick_ix + 1) % len(state.library_rows)
            sync_library_scroll()
        elif key in (10, 13) and state.library_rows:
            try:
                pick = state.library_rows[state.library_pick_ix]
                if state.library_mode == "playlists":
                    # Enter on playlist drills into its track list.
                    pid = pick.get("id") or ""
                    pname = pick.get("name") or "Playlist"
                    load_library_playlist_tracks(pid, pname)
                    state.status = (
                        f"{len(state.library_rows)} tracks in {state.library_playlist_name}"
                        if state.library_rows
                        else f"No tracks in {state.library_playlist_name}"
                    )
                else:
                    # Enter on track starts playlist context at this row (iPod-like order).
                    play_playlist_track_in_order(sp, state.library_playlist_id, pick["uri"], pick)
                    invalidate_now_playing_cache()
                    state.status = ellip_tw(
                        "Playing from playlist: " + pick.get("name", "?"),
                        80,
                    )
            except Exception as e:
                state.status = f"Error: {e}"
        elif key in (27, curses.KEY_LEFT):
            # Back from tracks to playlist list without leaving Library.
            if state.library_mode == "tracks":
                load_library_preview()
                state.status = (
                    f"{len(state.library_rows)} playlists"
                    if state.library_rows
                    else "No playlists from Spotify"
                )
        return True

    elif state.screen == "volume":
        # Enter applies typed Spotify volume value.
        if key in [10, 13]:
            if state.volume_text.strip():
                try:
                    v = int(state.volume_text.strip())
                    if v < 0 or v > 100:
                        state.status = "Spotify volume must be 0–100."
                    else:
                        sp.volume(v)
                        invalidate_volume_line_cache()
                        state.status = volume_meter_line(force=True)
                except ValueError:
                    state.status = "Spotify: digits 0–100 only."
                except Exception as e:
                    state.status = f"Spotify: {e}"
            else:
                state.status = volume_meter_line(force=True)

        elif key in (ord("+"), ord("=")):
            # Mac output volume up one step.
            try:
                nudge_mac_volume(1)
                invalidate_volume_line_cache()
                state.status = volume_meter_line(force=True)
            except Exception as e:
                state.status = f"Mac volume: {e}"

        elif key == ord("-"):
            # Mac output volume down one step.
            try:
                nudge_mac_volume(-1)
                invalidate_volume_line_cache()
                state.status = volume_meter_line(force=True)
            except Exception as e:
                state.status = f"Mac volume: {e}"

        elif key in [curses.KEY_BACKSPACE, 127, 8]:
            # Remove one digit from volume input.
            state.volume_text = state.volume_text[:-1]

        elif chr(key).isdigit() and len(state.volume_text) < 3:
            # Accept up to 3 digits (0-100 validated on submit).
            state.volume_text += chr(key)

    elif state.screen == "queue":
        # Queue refresh key.
        if key == ord("r"):
            load_queue_preview()
            state.status = (
                f"{len(state.queue_rows)} up next"
                if state.queue_rows and not state.queue_error
                else (ellip_tw(state.queue_error, 80) if state.queue_error else "No upcoming tracks")
            )
        elif key in (curses.KEY_UP, ord("w")):
            # Queue viewport scroll up.
            if state.queue_rows:
                state.queue_scroll = max(0, state.queue_scroll - 1)
        elif key in (curses.KEY_DOWN, ord("s")):
            # Queue viewport scroll down.
            if state.queue_rows:
                max_scr = max(0, len(state.queue_rows) - QUEUE_VISIBLE_ROWS)
                state.queue_scroll = min(max_scr, state.queue_scroll + 1)

    return True
