from utility import default_port, enc, dec

from serial import Serial
from time import sleep
import atexit
from signal import signal, SIGINT
from threading import Event, Thread
print(""""
  _____ _    _       _______            _____  _____  _      _____ _____       _______ _____ ____  _   _ 
 / ____| |  | |   /\|__   __|     /\   |  __ \|  __ \| |    |_   _/ ____|   /\|__   __|_   _/ __ \| \ | |
| |    | |__| |  /  \  | |       /  \  | |__) | |__) | |      | || |       /  \  | |    | || |  | |  \| |
| |    |  __  | / /\ \ | |      / /\ \ |  ___/|  ___/| |      | || |      / /\ \ | |    | || |  | | . ` |
| |____| |  | |/ ____ \| |     / ____ \| |    | |    | |____ _| || |____ / ____ \| |   _| || |__| | |\  |
 \_____|_|  |_/_/    \_\_|    /_/    \_\_|    |_|    |______|_____\_____/_/    \_\_|  |_____\____/|_| \_|

by Mélina Sladic & Lukas Probst.

Send messages between machines using the Arduino VLC devices as transceiver.\n
""")

BAUDRATE = 115200
### User input
DEFAULT_PORT = default_port()
DEFAULT_ADDRESS = "FF"

# Sets defaults for the microcontroller
def serial_setup(port: str, address: str) -> Serial:
    # Open the serial port and reset the device
    try:
        connection = Serial(port=port, baudrate=BAUDRATE, timeout=1)
    except:
        print(f"Could not open port {port}. Please try again.")
        exit()
    sleep(2)
    # Set the device address (in hex)
    connection.write(enc(f"a[{address}]\n"))
    sleep(0.1)
    assert dec(connection.read_until()) == f"a[{address}]\n"
    # Set the # of retransmissions to 5
    connection.write(enc("c[1,0,5]\n"))
    sleep(0.1)
    assert dec(connection.read_until()) == "c[1,0,5]\n"
    # Set the FEC threshold to 30
    connection.write(enc("c[0,1,30]\n"))
    sleep(0.1)
    assert dec(connection.read_until()) == "c[0,1,30]\n"
    return connection

try:
    input_port = input(f"Type in the serial port to be used (default is {DEFAULT_PORT}): ") or DEFAULT_PORT
    input_address = input(f"Type in the hex-encoded address you want to transmit to (default is {DEFAULT_ADDRESS}): ") or DEFAULT_ADDRESS

    print("Creating a serial connection to the transceiver...")
    serial = serial_setup(input_port, input_address)
    print("Connected.")
# writing the different exception class to catch/ handle the exception
except EOFError:
    print('\nEOF exception, please enter something and try again.')
except KeyboardInterrupt:
    print('\nProgram terminated...')



