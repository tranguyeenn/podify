from podify.config import sp
from podify.commands import next_track, pause, play, previous

from podify.ui import state
from podify.ui.constants import main_menu, playback_menu
from podify.ui.readouts import (
    invalidate_now_playing_cache,
    invalidate_volume_line_cache,
    now_play_line,
    volume_meter_line,
)
from podify.ui.sync import load_queue_preview, reset_search_pick
from podify.ui.text_layout import ellip_tw


def select_main():
    choice = main_menu[state.selected]

    if choice == "Now Playing":
        state.screen = "now"
        state.status = now_play_line(force=True)

    elif choice == "Playback":
        state.screen = "playback"
        state.selected = 0

    elif choice == "Search":
        state.screen = "search"
        reset_search_pick()

    elif choice == "Queue":
        state.screen = "queue"
        load_queue_preview()
        if state.queue_error:
            state.status = ellip_tw(state.queue_error, 80)
        else:
            state.status = (
                f"{len(state.queue_rows)} up next"
                if state.queue_rows
                else "No upcoming tracks from API"
            )

    elif choice == "Volume":
        state.screen = "volume"
        invalidate_volume_line_cache()
        state.status = volume_meter_line(force=True)

    elif choice == "Help":
        state.screen = "help"

    elif choice == "Quit":
        return False

    return True


def select_playback():
    choice = playback_menu[state.selected]

    try:
        if choice == "Play":
            play(sp)
            invalidate_now_playing_cache()
            state.status = now_play_line(force=True)

        elif choice == "Pause":
            pause(sp)
            invalidate_now_playing_cache()
            state.status = "Paused"

        elif choice == "Next Track":
            next_track(sp)
            invalidate_now_playing_cache()
            state.status = now_play_line(force=True)

        elif choice == "Previous Track":
            previous(sp)
            invalidate_now_playing_cache()
            state.status = now_play_line(force=True)

        elif choice == "Back":
            state.screen = "main"
            state.selected = 0

    except Exception as e:
        state.status = f"Error: {e}"

    return True


def go_back():
    reset_search_pick()
    state.search_text = ""
    state.screen = "main"
    state.selected = 0
