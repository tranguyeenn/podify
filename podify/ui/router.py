from podify.ui import state
from podify.ui.constants import main_menu, playback_menu
from podify.ui.screen_help import draw_help
from podify.ui.screen_menu import draw_menu
from podify.ui.screen_now_playing import draw_now_playing
from podify.ui.screen_queue import draw_queue
from podify.ui.screen_search import draw_search
from podify.ui.screen_volume import draw_volume


def draw(stdscr):
    if state.screen == "main":
        draw_menu(stdscr, "Podify", main_menu)
    elif state.screen == "playback":
        draw_menu(stdscr, "Playback", playback_menu)
    elif state.screen == "now":
        draw_now_playing(stdscr)
    elif state.screen == "search":
        draw_search(stdscr)
    elif state.screen == "volume":
        draw_volume(stdscr)
    elif state.screen == "queue":
        draw_queue(stdscr)
    elif state.screen == "help":
        draw_help(stdscr)
