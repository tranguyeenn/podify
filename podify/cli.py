"""Interactive command-line loop for Podify controls."""

from colorama import init

from podify.commands import current, handle_search, handle_volume, next_track, pause, play, previous
from podify.config import sp
from podify.display import show_help
from podify.mac_controls import handle_mac_volume

init(autoreset=True)


def main() -> None:
    # Main REPL loop for typed Spotify commands.
    print("Type 'help' to see available commands.")

    while True:
        user_input = input("spotify> ").strip()

        if not user_input:
            continue

        # Tokenize into command + optional args.
        parts = user_input.split()
        cmd = parts[0].lower()
        args = parts[1:]

        # Command dispatcher for CLI mode.
        if cmd in ["help", "h"]:
            show_help()
        elif cmd == "now":
            current(sp)
        elif cmd in ["pause", "ps"]:
            pause(sp)
        elif cmd in ["next", "n"]:
            next_track(sp)
        elif cmd in ["previous", "prev"]:
            previous(sp)
        elif cmd in ["play", "p"]:
            play(sp)
        elif cmd == "volume":
            handle_volume(sp, args)
        elif cmd == "macvol":
            handle_mac_volume(args)
        elif cmd == "search":
            handle_search(sp, args)
        elif cmd in ["exit", "quit", "q"]:
            print("Exiting...")
            break
        else:
            print("Unknown command. Type 'help'.")


if __name__ == "__main__":
    main()
