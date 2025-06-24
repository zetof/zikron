from curses import wrapper
from time import sleep
from lpd8 import LPD8


def set_bpm(stdscr, val):
    bpm = 40 + int(260 * val / 127)
    stdscr.addstr(0, 0, str(bpm))


def main(stdscr):
    delay = .001
    looping = True
    running = False
    sending = True
    bpm = 0

    stdscr.nodelay(True)

    while looping:
        try:
            key = str(stdscr.getkey())
            if key == 'q':
                looping = False
        except Exception:
            cmd, val = lpd8.read_midi()
            match cmd:
                case 1:
                    running = not running
                case 2:
                    sending = not sending
                case 3:
                    bpm = set_bpm(stdscr, val)
        sleep(delay)


lpd8 = LPD8()
if lpd8.connect():
    wrapper(main)
