import rtmidi


class LPD8():
    NAME = 'LPD8'
    DELAY = 1
    NOTE_ON = 143
    CTRL = 175

    def __init__(self, pgm=4,
                 start_stop=67,
                 rewind=60,
                 hold=69,
                 tempo_c=1,
                 tempo_f=5):
        self._cmd = self.NOTE_ON + pgm
        self._ctrl = self.CTRL + pgm
        self._start_stop = start_stop
        self._rewind = rewind
        self._hold = hold
        self._tempo_c = tempo_c
        self._tempo_f = tempo_f

    def read_midi(self):
        msg = self._midi_in.get_message()
        if msg is not None:
            cmd = msg[0][0]
            ctrl = msg[0][1]
            if cmd == self._cmd and ctrl == self._start_stop:
                return 1, 0
            if cmd == self._cmd and ctrl == self._rewind:
                return 2, 0
            if cmd == self._cmd and ctrl == self._hold:
                return 3, 0
            if cmd == self._ctrl and ctrl == self._tempo_c:
                return 4, msg[0][2]
            if cmd == self._ctrl and ctrl == self._tempo_f:
                return 5, msg[0][2]
        return False, 0

    def create_virtual_port(self):
        midi_in = rtmidi.MidiIn()
        self._midi_in = midi_in.open_virtual_port("zikron_input")
