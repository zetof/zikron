import rtmidi
import curses
from threading import Thread
from time import sleep


class Clock(Thread):

    _TEMPO = [
        [['O O O O 0'],
         ['O       O'],
         ['O   0   O'],
         ['O       O'],
         ['O O O O O']],
        [['O O O O O'],
         ['         '],
         ['    {}    '],
         ['         '],
         ['         ']],
        [['    O O O'],
         ['        O'],
         ['    {}   O'],
         ['         '],
         ['         ']],
        [['        O'],
         ['        O'],
         ['    {}   O'],
         ['        O'],
         ['        O']],
        [['         '],
         ['         '],
         ['    {}   O'],
         ['        O'],
         ['    O O O']],
        [['         '],
         ['         '],
         ['    {}    '],
         ['         '],
         ['O O O O O']],
        [['         '],
         ['         '],
         ['O   {}    '],
         ['O        '],
         ['O O O    ']],
        [['O        '],
         ['O        '],
         ['O   {}    '],
         ['O        '],
         ['O        ']],
        [['O O O    '],
         ['O        '],
         ['O   {}    '],
         ['         '],
         ['         ']]
    ]

    def __init__(self, stdscr, bpm, line, col, color):
        self._stdscr = stdscr
        self._bpm = bpm
        self._delay = self._set_delay(bpm)
        self._line = line
        self._col = col
        self._color = color
        self._step = 0
        self._beat = 1
        self._running = True
        self._looping = False
        self._print_tempo(-3)
        Thread.__init__(self)

    def _set_delay(self, bpm):
        return 2.5 / bpm

    def _print_tempo(self, index):
        if index % 3 == 0:
            for i, tempo in enumerate(self._TEMPO[int(index / 3) + 1]):
                if i == 2:
                    string = tempo[0].format(self._beat)
                else:
                    string = tempo[0]
                self._stdscr.addstr(self._line + i,
                                    self._col,
                                    string,
                                    curses.color_pair(self._color))

    def set_bpm(self, hold, bpm):
        if not hold:
            self._bpm = bpm
            self._delay = self._set_delay(bpm)

    def change_looping(self):
        if self._looping:
            self._midi_out.send_message([0xfc])
        else:
            if self._beat == 0 and self._step == 0:
                self._midi_out.send_message([0xfa])
            else:
                self._midi_out.send_message([0xfb])
        self._looping = not self._looping

    def rewind(self):
        self._step = 0
        self._beat = 1
        self._midi_out.send_message([0xfa])
        self._looping = True

    def run(self):
        while self._running:
            self._midi_out.send_message([0xf8])
            if self._looping:
                self._step += 1
                if self._step > 23:
                    self._step = 0
                    self._beat += 1
                    if self._beat > 4:
                        self._beat = 1
                self._print_tempo(self._step)
            sleep(self._delay)

    def stop(self):
        self._running = False

    def create_virtual_port(self):
        midi_out = rtmidi.MidiOut()
        self._midi_out = midi_out.open_virtual_port('zikron_clock')
        self._midi_out.send_message([0xfc])
