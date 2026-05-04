"""UI constants: dimensions, timing, and static menu labels."""

#Shared layout width for iPod frame body text.
FRAME_INNER_W = 38
#Shared layout width for wheel/body center sections.
WHEEL_INNER_W = 18
#Keep the list height compact so it fits smaller terminal windows.
LIBRARY_ROWS = 8
#Queue viewport row count (scroll handles the rest).
QUEUE_VISIBLE_ROWS = 7
#Small cache/display timing helper used by UI readouts.
DISPLAY_TTL_S = 2.5

#Main iPod home menu order (used by selection index).
main_menu = [
    "Now Playing",
    "Playback",
    "Library",
    "Queue",
    "Volume",
    "Help",
    "Quit",
]

#Playback submenu actions.
playback_menu = [
    "Play",
    "Pause",
    "Next Track",
    "Previous Track",
    "Back",
]
