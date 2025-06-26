import rtmidi


class LPD8():
    NAME = 'LPD8'
    DELAY = 1
    NOTE_ON = 143
    CTRL = 175

    def __init__(self, pgm=4, start_stop=67, send=60, tempo=1):
        self._cmd = self.NOTE_ON + pgm
        self._ctrl = self.CTRL + pgm
        self._start_stop = start_stop
        self._send = send
        self._tempo = tempo

    def read_midi(self):
        msg = self._midi_in.get_message()
        if msg is not None:
            cmd = msg[0][0]
            ctrl = msg[0][1]
            if cmd == self._cmd and ctrl == self._start_stop:
                return 1, 0
            if cmd == self._cmd and ctrl == self._send:
                return 2, 0
            if cmd == self._ctrl and ctrl == self._tempo:
                return 3, msg[0][2]
        return False, 0

    def create_ports(self):
        midi_in = rtmidi.MidiIn()
        midi_out = rtmidi.MidiOut()
        self._midi_in = midi_in.open_virtual_port("zikron_input")
        self._midi_out = midi_out.open_virtual_port("zikron_clock")
