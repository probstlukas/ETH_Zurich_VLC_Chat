from threading import Event
from broadcast import Broadcast
from keyboard import add_hotkey

class CLI():

    def __init__(self, exit_event: Event, broadcast: Broadcast):
        self.exit_event = exit_event
        self.broadcast = broadcast
        self.is_accepting_input = False
        # press enter to accept input
        add_hotkey('enter', self.accept_input)

    def accept_input(self):
        self.is_accepting_input = True

    def event_loop(self):
        while not self.exit_event.is_set(): #while not terminate
            # Attempt to receive a message.
            received_message = self.broadcast.get_message()
            if received_message:
                (message, sender) = received_message
                print(f"{sender}: {message}")
            # Listen for user input, and send a message.
            if self.is_accepting_input:
                input()
                message = input("> ")
                if len(message) <= 200:
                    self.broadcast.put_transmit_queue(message)
                else:
                    print("Maximum message size is 200 characters.")
                self.is_accepting_input = False