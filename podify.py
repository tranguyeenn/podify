import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from spotipy.exceptions import SpotifyException
from colorama import init, Fore, Style

init(autoreset=True)

load_dotenv()

scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="http://127.0.0.1:8888/callback"
    )
)

def current():
    current_track = sp.current_user_playing_track()
    
    if current_track is not None:
        track_name = current_track['item']['name']
        artists = ', '.join([artist['name'] for artist in current_track['item']['artists']])
        print(Style.BRIGHT + Fore.GREEN + f"🎧 Currently playing: {track_name} by {artists}")

    else:
        print("No track is currently playing.")

def pause():
    sp.pause_playback()
    print("⏸ paused.")

def next():
    sp.next_track()
    print("⏭ skipped.")


def previous():
    try:
        sp.previous_track()
        print("⏮ previous track")
    except SpotifyException as e:
        if e.http_status == 403:
            print()
            print(Fore.RED + "Spotify blocked previous track for this playback.")
            print(Fore.RED+ "Try playing from a normal playlist/album, not queue/radio/podcast/ad.")
        else:
            print(Fore.RED + "Spotify error:", e)

def play():
    sp.start_playback()
    print("🎧 Playback started.")

def exit():
    print("Exiting...")
    quit()

while True:
    cmd = input("spotify> ").strip().lower()

    if cmd == "now":
        current()
    elif cmd == "pause":
        pause()
    elif cmd == "next":
        next()
    elif cmd == "previous":
        previous()
    elif cmd == "play":
        play()
    elif cmd == "exit":
        exit()
    else:
        print("Commands: now, pause, next, previous, play, exit")