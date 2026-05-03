from colorama import init

from config import sp
from commands import current, pause, next_track, previous, play, handle_volume, handle_search
from mac_controls import handle_mac_volume
from display import show_help

init(autoreset=True)

print("Type 'help' to see available commands.")

while True:
    user_input = input("spotify> ").strip()

    if not user_input:
        continue

    parts = user_input.split()
    cmd = parts[0].lower()
    args = parts[1:]

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