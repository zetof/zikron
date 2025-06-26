import curses
from curses import wrapper
from time import sleep
from lpd8 import LPD8
from digits import Digits


def set_bpm(stdscr, val):
    bpm = 40 + int(254 * val / 127)
    Digits.print_number(stdscr, 2, 2, 1, bpm, 3)


def main(stdscr):
    delay = .001
    looping = True
    running = False
    sending = True
    bpm = 0

    stdscr.nodelay(True)
    curses.curs_set(0)
    curses.init_pair(1, 86, 0)

    lpd8 = LPD8()
    lpd8.create_ports()

    digits = Digits()
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


wrapper(main)
