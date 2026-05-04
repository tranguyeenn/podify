"""CLI-only text rendering helpers (help menu, etc.)."""

def show_help():
    # Keep this in sync with commands exposed in cli.py.
    print("""
    Commands:
        now              Show current song
        play/p           Resume playback
        pause/ps         Pause playback
        next/n           Skip to next track
        previous/prev    Go to previous track
        volume 0-100     Set Spotify volume
        macvol 0-100     Set Mac system volume
        search <query>   Search Spotify for a track, album, or artist
        help/h           Show this menu
        quit/q/ exit     Exit
""")