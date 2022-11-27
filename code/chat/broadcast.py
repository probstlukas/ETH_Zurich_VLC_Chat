
from sys import path
# adding shared folder to the system path
path.append('../shared')
from threading import Event
from serial import Serial, SerialException
from queue import Queue, Empty
from utility import enc, dec

### Transmit messages and receive messages by listening for incoming messages from its queue
class Broadcast():

    # Constructor
    def __init__(self, exit_event: Event, serial: Serial, dest: str):
        self.exit_event = exit_event
        self.serial = serial
        self.dest = dest
        self.transmit_queue = Queue(maxsize=10)
        self.receive_queue = Queue(maxsize=10)

    # Put message into queue for transmission
    def put_transmit_queue(self, message: str):
        self.transmit_queue.put((message, self.dest), timeout=0.1)

    # Remove and return a message from the queue
    def get_message(self) -> str | None:
        try:
            message = self.receive_queue.get(timeout=0.1)
            self.receive_queue.task_done()
            return message
        except Empty:
            return None

    # Dispatches the oldest message from the transmit queue
    def send(self):
        try:
            (message, dest) = self.transmit_queue.get(timeout=0.1)
            self.transmit_queue.task_done()
        except Empty:
            return 
        enc_message = enc(f"m[{message}\0,{dest}]\n")
        self.serial.write(enc_message)
        response = self.receive()
        # m[msg,dest] returns 1 on success
        assert "1" in response
        # TODO: necessary? Probably not needed
        while self.receive() != "m[D]":
            pass

    def receive(self) -> str:
        dec_message = dec(self.serial.read_until()).strip()
        # R: Ready To Send (RTS), D: Data
        if dec_message.startswith("m[R,D,"):
            # TODO: Why 6th and last element?
            self.receive_queue.put((dec_message[6:-1].strip(), self.dest))
        return dec_message

     # Running infinite loop
    def event_loop(self):
        try:
            while not self.exit_event.is_set():
                self.receive()
                self.send()
        except SerialException:
            self.exit_event.set()