import curses

from podify.config import sp
from podify.commands import next_track, pause, play_track_uri, previous, search_tracks
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
from podify.ui.sync import load_queue_preview, reset_search_pick, sync_search_scroll
from podify.ui.text_layout import ellip_tw


def handle_key(key) -> bool:
    current_items = main_menu if state.screen == "main" else playback_menu

    if key == ord("q"):
        return False

    if key == ord("m"):
        go_back()
        return True

    if state.screen in ["main", "playback"]:
        if key in [ord("w"), curses.KEY_UP]:
            state.selected = (state.selected - 1) % len(current_items)

        elif key in [ord("s"), curses.KEY_DOWN]:
            state.selected = (state.selected + 1) % len(current_items)

        elif key in [10, 13]:
            if state.screen == "main":
                return select_main()
            return select_playback()

    elif state.screen == "now":
        if key == ord(" "):
            try:
                pause(sp)
                invalidate_now_playing_cache()
                state.status = "Paused"
            except Exception as e:
                state.status = f"Error: {e}"

        elif key in [ord("a"), curses.KEY_LEFT]:
            try:
                previous(sp)
                invalidate_now_playing_cache()
                state.status = now_play_line(force=True)
            except Exception as e:
                state.status = f"Error: {e}"

        elif key in [ord("d"), curses.KEY_RIGHT]:
            try:
                next_track(sp)
                invalidate_now_playing_cache()
                state.status = now_play_line(force=True)
            except Exception as e:
                state.status = f"Error: {e}"

    elif state.screen == "search":
        if state.search_pick_mode and state.search_results:
            if key in (curses.KEY_UP, ord("w")):
                state.search_pick_ix = (
                    state.search_pick_ix - 1 if state.search_pick_ix else len(state.search_results) - 1
                )
                sync_search_scroll()
            elif key in (curses.KEY_DOWN, ord("s")):
                state.search_pick_ix = (state.search_pick_ix + 1) % len(state.search_results)
                sync_search_scroll()
            elif key in (10, 13):
                try:
                    pick = state.search_results[state.search_pick_ix]
                    play_track_uri(sp, pick["uri"], pick)
                    invalidate_now_playing_cache()
                    state.status = ellip_tw(
                        "Playing " + pick.get("name", "?"),
                        80,
                    )
                    reset_search_pick()
                    state.search_text = ""
                except Exception as e:
                    state.status = f"Error: {e}"
            elif key in (27, 9):
                reset_search_pick()
                state.status = "Query"
            elif key in (curses.KEY_BACKSPACE, 127, 8):
                reset_search_pick()
                state.search_text = state.search_text[:-1]
                state.status = ""
            elif 32 <= key <= 126:
                pass
            return True

        if key in (10, 13):
            query = state.search_text.strip()
            if not query:
                state.status = "Type something to search."
                return True
            try:
                state.search_results = search_tracks(sp, query, limit=30)
                if not state.search_results:
                    reset_search_pick()
                    state.status = "No results."
                    return True
                state.search_pick_mode = True
                state.search_pick_ix = 0
                state.search_scroll = 0
                sync_search_scroll()
                state.status = f"{len(state.search_results)} results"
            except Exception as e:
                reset_search_pick()
                state.status = f"Error: {e}"
            return True

        elif key in (27,):
            state.search_text = ""
            reset_search_pick()
            state.status = ""
            return True

        elif key in [curses.KEY_BACKSPACE, 127, 8]:
            state.search_text = state.search_text[:-1]

        elif 32 <= key <= 126:
            state.search_text += chr(key)

        return True

    elif state.screen == "volume":
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
            try:
                nudge_mac_volume(1)
                invalidate_volume_line_cache()
                state.status = volume_meter_line(force=True)
            except Exception as e:
                state.status = f"Mac volume: {e}"

        elif key == ord("-"):
            try:
                nudge_mac_volume(-1)
                invalidate_volume_line_cache()
                state.status = volume_meter_line(force=True)
            except Exception as e:
                state.status = f"Mac volume: {e}"

        elif key in [curses.KEY_BACKSPACE, 127, 8]:
            state.volume_text = state.volume_text[:-1]

        elif chr(key).isdigit() and len(state.volume_text) < 3:
            state.volume_text += chr(key)

    elif state.screen == "queue":
        if key == ord("r"):
            load_queue_preview()
            state.status = (
                f"{len(state.queue_rows)} up next"
                if state.queue_rows and not state.queue_error
                else (ellip_tw(state.queue_error, 80) if state.queue_error else "No upcoming tracks")
            )
        elif key in (curses.KEY_UP, ord("w")):
            if state.queue_rows:
                state.queue_scroll = max(0, state.queue_scroll - 1)
        elif key in (curses.KEY_DOWN, ord("s")):
            if state.queue_rows:
                max_scr = max(0, len(state.queue_rows) - QUEUE_VISIBLE_ROWS)
                state.queue_scroll = min(max_scr, state.queue_scroll + 1)

    return True
