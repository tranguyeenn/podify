from spotipy.exceptions import SpotifyException
from colorama import Fore, Style

def current(sp):
    current_track = sp.current_user_playing_track()

    if current_track is not None and current_track["item"] is not None:
        track_name = current_track["item"]["name"]
        artists = ", ".join(
            artist["name"] for artist in current_track["item"]["artists"]
        )

        print(
            Style.BRIGHT
            + Fore.GREEN
            + f"🎧 Currently playing: {track_name} by {artists}"
        )
    else:
        print("No track is currently playing.")

def pause(sp):
    sp.pause_playback()
    print("⏸ paused.")

def next_track(sp):
    sp.next_track()
    print("⏭ skipped.")

def previous(sp):
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
    try:
        sp.start_playback()
        print("▶️  Playback started.")
    except SpotifyException as e:
        print(Fore.RED + f"Spotify error: {e}")

def handle_volume(sp, args):
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

def handle_search(sp, args):
    if not args:
        print("Usage: search <song name>")
        return
    query = " ".join(args)

    try:
        results = sp.search(q=query, type="track", limit=10)

        tracks = results["tracks"]["items"]

        if not tracks:
            print("No results found.")
            return

        print('\n',"Search results:")

        for i, track in enumerate(tracks, start=1):
            track_name = track["name"]
            artists = ", ".join(artist["name"] for artist in track["artists"])
            print(f"{i}. {track_name} by {artists}")
        
        choice = input("Enter the number of the track to play (or 'cancel'): ").strip()

        if not choice:
            return
        index = int(choice) - 1
        if index < 0 or index >= len(tracks):
            print("Invalid choice.")
            return
        
        uri = tracks[index]["uri"]
        sp.start_playback(uris=[uri])

        print("▶️ Playing selection.")

    except Exception as e:
        print(Fore.RED + f"Searched failed: {e}")
        