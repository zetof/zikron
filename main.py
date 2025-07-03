import curses
from curses import wrapper
from time import sleep
from lpd8 import LPD8
from clock import Clock
from digits import Digits


def set_bpm(stdscr, hold, val_c, val_f):
    bpm = 30 + int(262 * val_c / 127 + 8 * val_f / 127)
    color = 1 if not hold else 2
    Digits.print_number(stdscr, 2, 2, color, bpm, 3)
    return bpm


def main(stdscr):
    delay = .001
    running = True
    hold = False
    val_c = 64
    val_f = 64

    stdscr.nodelay(True)
    curses.curs_set(0)
    curses.init_pair(1, 227, 0)
    curses.init_pair(2, 9, 0)
    curses.init_pair(3, 119, 0)

    lpd8 = LPD8()
    lpd8.create_virtual_port()

    clock = Clock(stdscr, 120, 2, 22, 3)
    clock.create_virtual_port()
    clock.start()

    bpm = set_bpm(stdscr, hold, val_c, val_f)
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
                    clock.rewind()
                case 3:
                    hold = not hold
                    color = 1 if not hold else 2
                    Digits.print_number(stdscr, 2, 2, color, bpm, 3)
                    clock.set_bpm(hold, bpm)
                case 4:
                    val_c = val
                    bpm = set_bpm(stdscr, hold, val_c, val_f)
                    clock.set_bpm(hold, bpm)
                case 5:
                    val_f = val
                    bpm = set_bpm(stdscr, hold, val_c, val_f)
                    clock.set_bpm(hold, bpm)
        sleep(delay)


wrapper(main)
