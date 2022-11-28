from sys import path
# Adding shared folder to the system path
path.append('../shared')

from utility import default_port, serial_config  
from serial import Serial
from signal import signal, SIGINT
from threading import Event, Thread
from broadcast import Broadcast
from cli import CLI


print("""
  _____ _    _       _______            _____  _____  _      _____ _____       _______ _____ ____  _   _ 
 / ____| |  | |   /\|__   __|     /\   |  __ \|  __ \| |    |_   _/ ____|   /\|__   __|_   _/ __ \| \ | |
| |    | |__| |  /  \  | |       /  \  | |__) | |__) | |      | || |       /  \  | |    | || |  | |  \| |
| |    |  __  | / /\ \ | |      / /\ \ |  ___/|  ___/| |      | || |      / /\ \ | |    | || |  | | . ` |
| |____| |  | |/ ____ \| |     / ____ \| |    | |    | |____ _| || |____ / ____ \| |   _| || |__| | |\  |
 \_____|_|  |_/_/    \_\_|    /_/    \_\_|    |_|    |______|_____\_____/_/    \_\_|  |_____\____/|_| \_|

by Mélina Sladic & Lukas Probst.

Send messages between machines using the Arduino VLC devices as transceiver.\n
""")

### User input
DEFAULT_PORT = default_port()
DEFAULT_SRC_ADDRESS = "AA"
DEFAULT_DEST_ADDRESS = "FF"

try:
    port = input(f"Enter the serial port to be used (default is {DEFAULT_PORT}): ") or DEFAULT_PORT
    src_address = input(f"Enter the hex-encoded address you want to transmit from (default is {DEFAULT_SRC_ADDRESS}): ") or DEFAULT_SRC_ADDRESS

    print("Creating a serial connection to the transceiver...")
    serial = serial_config(port, src_address)
    print("Connected.")

    dest_address = input(f"Enter the hex-encoded address you want to send messages to (default is the broadcast address {DEFAULT_DEST_ADDRESS}): ") or DEFAULT_DEST_ADDRESS
    print("Press ENTER to open the message prompt.\n")
# Writing the different exception class to catch/handle the exception
except EOFError:
    print('\nEOF exception, please enter something and try again.')
except KeyboardInterrupt:
    print('\nProgram terminated...')

exit_event = Event()
exit_event.clear()
def signal_handler(sig, frame):
    exit_event.set()
    print('\nProgram terminated...')
    exit(0)
signal(SIGINT, signal_handler)

broadcast = Broadcast(exit_event, serial, dest_address)
broadcast_thread = Thread(target=broadcast.event_loop)
broadcast_thread.start()

cli = CLI(exit_event, broadcast)
cli.event_loop()

broadcast_thread.join()
