import curses
from curses import wrapper
from time import sleep
from lpd8 import LPD8
from clock import Clock
from digits import Digits


def set_bpm(stdscr, val):
    bpm = 20 + 2 * val
    Digits.print_number(stdscr, 2, 2, 1, bpm, 3)
    return bpm


def main(stdscr):
    delay = .001
    running = True
    sending = True
    bpm = 120

    stdscr.nodelay(True)
    curses.curs_set(0)
    curses.init_pair(1, 227, 0)
    curses.init_pair(2, 119, 0)

    lpd8 = LPD8()
    lpd8.create_virtual_port()

    clock = Clock(stdscr, 120, 3, 22, 2)
    clock.create_virtual_port()
    clock.start()

    Digits.print_number(stdscr, 2, 2, 1, bpm, 3)

    while running:
        try:
            key = str(stdscr.getkey())
            if key == 'q':
                clock.stop()
                running = False
        except Exception:
            cmd, val = lpd8.read_midi()
            match cmd:
                case 1:
                    clock.change_looping()
                case 2:
                    sending = not sending
                case 3:
                    bpm = set_bpm(stdscr, val)
                    clock.set_bpm(bpm)
        sleep(delay)


wrapper(main)
