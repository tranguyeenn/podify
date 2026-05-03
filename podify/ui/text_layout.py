import unicodedata

from podify.ui.constants import FRAME_INNER_W


def char_display_width(ch: str) -> int:
    if len(ch) != 1:
        return sum(char_display_width(x) for x in ch)
    return 2 if unicodedata.east_asian_width(ch) in ("F", "W") else 1


def text_width(s: str) -> int:
    return sum(char_display_width(c) for c in str(s))


def pad_to_width(s: str, cols: int) -> str:
    return s + (" " * max(0, cols - text_width(s)))


def truncate_to_width(s: str, cols: int) -> str:
    out = []
    w = 0
    for c in str(s):
        dc = char_display_width(c)
        if w + dc > cols:
            break
        out.append(c)
        w += dc
    return "".join(out)


def ellip_tw(s: str, cols: int) -> str:
    one = " ".join(str(s).replace("\n", " ").replace("\r", " ").split())
    if text_width(one) <= cols:
        return one
    if cols <= 3:
        return truncate_to_width(one, cols)
    tail = "..."
    avail = cols - text_width(tail)
    if avail < 1:
        return truncate_to_width(one, cols)
    return truncate_to_width(one, avail).rstrip() + tail


def inner_left(s: str) -> str:
    return pad_to_width(ellip_tw(s, FRAME_INNER_W), FRAME_INNER_W)


def inner_center(s: str) -> str:
    t = ellip_tw(s, FRAME_INNER_W)
    g = FRAME_INNER_W - text_width(t)
    if g <= 0:
        return pad_to_width(t, FRAME_INNER_W)
    ln = g // 2
    rn = g - ln
    return pad_to_width((" " * ln) + t + (" " * rn), FRAME_INNER_W)


def frame_top_rule() -> str:
    return "╭" + ("─" * FRAME_INNER_W) + "╮"


def frame_mid_rule() -> str:
    return "├" + ("─" * FRAME_INNER_W) + "┤"


def frame_bottom_rule() -> str:
    return "╰" + ("─" * FRAME_INNER_W) + "╯"
