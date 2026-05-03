import subprocess

def handle_mac_volume(args):
    if len(args) != 1:
        print("Usage: macvol <0-100>")
        return

    try:
        vol = int(args[0])

        if vol < 0 or vol > 100:
            print("Volume must be between 0 and 100.")
            return

        subprocess.run(
            ["osascript", "-e", f"set volume output volume {vol}"],
            check=True
        )

        print(f"Mac volume set to {vol}%")

    except ValueError:
        print("Volume must be a number.")
    except subprocess.CalledProcessError:
        print("Failed to change Mac volume.")