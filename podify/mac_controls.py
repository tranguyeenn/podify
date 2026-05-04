"""macOS output-volume helpers via osascript."""

import subprocess


def _osascript(source: str) -> str:
    # Centralized osascript runner with stderr/stdout surfaced on failure.
    r = subprocess.run(
        ["osascript", "-e", source],
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "osascript failed").strip())
    return r.stdout.strip()


def get_mac_output_volume() -> int:
    # Reads current system output volume as an integer percent.
    return int(float(_osascript("output volume of (get volume settings)")))


def set_mac_output_volume(vol: int) -> int:
    # Clamp to valid 0-100 then apply through AppleScript.
    v = max(0, min(100, int(vol)))
    subprocess.run(
        ["osascript", "-e", f"set volume output volume {v}"],
        check=True,
        capture_output=True,
        text=True,
    )
    return v


def nudge_mac_volume(delta: int, step: int = 6) -> int:
    """Change Mac speaker output volume by ±step blocks (clamp 0–100)."""
    cur = get_mac_output_volume()
    if delta < 0:
        return set_mac_output_volume(cur - step)
    if delta > 0:
        return set_mac_output_volume(cur + step)
    return cur


def handle_mac_volume(args):
    # CLI handler supports absolute values and relative up/down actions.
    if len(args) != 1:
        print("Usage: macvol <0-100|up|down>")
        return None

    a = str(args[0]).lower().strip()
    try:
        if a in ("up", "+", "louder"):
            v = nudge_mac_volume(1)
            print(f"Mac volume {v}%")
            return v
        if a in ("down", "-", "quieter"):
            v = nudge_mac_volume(-1)
            print(f"Mac volume {v}%")
            return v
        vol = int(a)
        v = set_mac_output_volume(vol)
        print(f"Mac volume set to {v}%")
        return v
    except ValueError:
        print("Volume must be 0–100, up, or down.")
    except Exception as e:
        print(f"Failed to change Mac volume: {e}")
    return None
