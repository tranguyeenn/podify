# 🎧 Podify — Spotify CLI Controller
Control Spotify directly from your terminal like a civilized engineer.

## Features
* Play/Pause music
* Skip to next/previous track
* View currently playing song
* Control playback from terminal
* Colored terminal output (because we have standards)
* The choice between a simple terminal commands or a simple terminal UI
* The queue is shown

## Demo
```bash
spotify> now
🎧 Ordinary Life - The Weeknd

spotify> pause
⏸ Paused

spotify> next
⏭ Skipped

spotify> previous
⏮ Previous track
```

## Requirements
* Python 3.10+
* Spotify Premium account (required for playback control)
* Spotify app running on a device

## Installation

Clone the repo:

```bash
git clone https://github.com/yourusername/podify.git
cd podify
```

Create virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Podify (Step-by-step)

Use these exact commands from the repo root:

```bash
cd /Users/trangnguyen/dev/podify
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Create `.env` in the repo root:

```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

Then run one of these:

```bash
# Text CLI
python3 -m podify

# iPod-style UI
python3 -m podify.ui
```

On first run, a browser window opens for Spotify auth. Approve access and return to terminal.

### Re-auth (important after scope updates)

If you get `Insufficient client scope` errors, clear cached token and log in again:

```bash
rm -f .cache
python3 -m podify.ui
```

## Setup (Spotify API)

1. Go to: https://developer.spotify.com/dashboard
2. Create a new app
3. Add redirect URI:

```text
http://127.0.0.1:8888/callback
```

4. Create a `.env` file:

```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

## Usage

Run the text CLI (from the repo root so imports resolve):

```bash
python3 -m podify
```

Run the iPod-style TUI:

```bash
python3 -m podify.ui
```

Available commands:
```text
now         -> show current track
play        -> resume playback
pause       -> pause playback
next        -> skip track
previous    -> go to previous track
volume      -> control mac volume or spotify volume
playlist    -> show playlist
quit        -> exit
```

## Notes
* Spotify must be open and actively playing music
* Some commands (like `previous`) may be restricted depending on playback context
* First run will open a browser for authentication

## Tech Stack
* Python
* Spotipy (Spotify Web API)
* Colorama (terminal styling)
* python-dotenv (loading env variables)
* subprocess (control mac volume)

## Future Improvements
* Real-time now-playing updates
* Keyboard shortcuts

## License
MIT
