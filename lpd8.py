import rtmidi
from threading import Thread
from time import sleep


class LPD8(Thread):
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
        self._delay = self.DELAY / 1000
        self.connect()

    def _get_midi_device(self, devices_list):
        midi_device = None
        midi_ports = devices_list.get_ports()
        if len(midi_ports) != 0:
            index = 0
            for name in midi_ports:
                if name.find(self.NAME) != -1:
                    devices_list.open_port(index)
                    midi_device = devices_list
                index += 1
        return midi_device

    def _read_midi(self):
        msg = self._midi_in.get_message()
        if msg is not None:
            cmd = msg[0][0]
            ctrl = msg[0][1]
            if cmd == self._cmd and ctrl == self._start_stop:
                print("START / STOP")
            elif cmd == self._cmd and ctrl == self._send:
                print("SEND")
            elif cmd == self._ctrl and ctrl == self._tempo:
                print("TEMPO: {}".format(msg[0][2]))

    def run(self):
        while self._running:
            self._read_midi()
            sleep(self._delay)

    def stop(self):
        self._running = False

    def is_running(self):
        return self._running

    def connect(self):
        self._midi_in = self._get_midi_device(rtmidi.MidiIn())
        self._midi_out = self._get_midi_device(rtmidi.MidiOut())
        if self._midi_in is not None and self._midi_out is not None:
            self._running = True
        else:
            self._running = False
            print("*** No LPD8 Controller found ***")
        Thread.__init__(self)
