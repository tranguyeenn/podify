"""Screen router: maps `state.screen` to draw function."""

from podify.ui import state
from podify.ui.constants import main_menu, playback_menu
from podify.ui.screen_help import draw_help
from podify.ui.screen_library import draw_library
from podify.ui.screen_menu import draw_menu
from podify.ui.screen_now_playing import draw_now_playing
from podify.ui.screen_queue import draw_queue
from podify.ui.screen_volume import draw_volume


def draw(stdscr):
    # Central screen switch for the iPod-style UI.
    # Keep branch order aligned with primary navigation hierarchy.
    if state.screen == "main":
        draw_menu(stdscr, "Podify", main_menu)
    elif state.screen == "playback":
        draw_menu(stdscr, "Playback", playback_menu)
    elif state.screen == "now":
        draw_now_playing(stdscr)
    elif state.screen == "library":
        # Library replaced the old Search flow for iPod-like UX.
        draw_library(stdscr)
    elif state.screen == "volume":
        draw_volume(stdscr)
    elif state.screen == "queue":
        draw_queue(stdscr)
    elif state.screen == "help":
        draw_help(stdscr)
