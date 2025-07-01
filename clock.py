import rtmidi
import curses
from threading import Thread
from time import sleep


class Clock(Thread):

    _TEMPO = [
        [[0, 1, 1],
         [1, 1, 1],
         [2, 1, 1]],
        [[0, 2, 1],
         [1, 1, 1],
         [2, 0, 1]],
        [[1, -1, 1],
         [1, 1, 1],
         [1, 3, 1]],
        [[0, 0, 1],
         [1, 1, 1],
         [2, 2, 1]]
    ]

    def __init__(self, stdscr, bpm, line, col, color):
        self._stdscr = stdscr
        self._bpm = bpm
        self._delay = self._set_delay(bpm)
        self._line = line
        self._col = col
        self._color = color
        self._step = 0
        self._running = True
        self._looping = False
        self._print_tempo(0)
        Thread.__init__(self)

    def _set_delay(self, bpm):
        return 2.5 / bpm

    def _print_tempo(self, index):
        for i in range(0, 3):
            self._stdscr.addstr(self._line + i, self._col - 1, " " * 5)
        for tempo in self._TEMPO[index]:
            self._stdscr.addstr(self._line + tempo[0],
                                self._col + tempo[1],
                                "O" * tempo[2],
                                curses.color_pair(self._color))

    def set_bpm(self, bpm):
        self._bpm = bpm
        self._delay = self._set_delay(bpm)

    def change_looping(self):
        if self._looping:
            self._midi_out.send_message([0xfc])
        else:
            self._midi_out.send_message([0xfb])
        self._looping = not self._looping

    def run(self):
        while self._running:
            self._midi_out.send_message([0xf8])
            if self._looping:
                self._step += 1
                if self._step > 23:
                    self._step = 0
                if self._step % 6 == 0:
                    self._print_tempo(int(self._step / 6))
            sleep(self._delay)

    def stop(self):
        self._running = False

    def create_virtual_port(self):
        midi_out = rtmidi.MidiOut()
        self._midi_out = midi_out.open_virtual_port("zikron_clock")
        self._midi_out.send_message([0xfc])
