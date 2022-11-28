from sys import platform
from glob import glob
from time import sleep
from serial import Serial

### Settings
BAUDRATE = 115200

# Returns a default serial port based on the OS being used
def default_port():  
    # Windows
    if platform.startswith("win"):
        return "COM9"
    # Linux
    elif platform.startswith("linux"):
        return next(iter(glob("/dev/tty[A-Za-z]*")), "none")
    # macOS
    elif platform.startswith("darwin"):
        return next(iter([x for x in glob("/dev/tty.*") if "usb" in x]), "none")
    else:
        return "none"

### Unicode strings are not supported, thus we need utility functions for encoding and decoding
def enc(string: str) -> bytes:
    return bytes(string, "ascii")

def dec(bytes: bytes) -> str:
    return bytes.decode("ascii")

# Sets defaults for the microcontroller
def serial_config(port: str, address: str) -> Serial:
    # Open the serial port and reset the device
    try:
        connection = Serial(port=port, baudrate=BAUDRATE, timeout=1)
    except:
        print(f"Port {port} could not be opened.")
        exit()
    sleep(2)
    # Set the device address (in hex)
    connection.write(enc(f"a[{address}]\n"))
    sleep(0.1) # Wait for settings to be applied
    assert dec(connection.read_until()) == f"a[{address}]\n"
    # Set the # of retransmissions to 5
    connection.write(enc("c[1,0,5]\n"))
    sleep(0.1) # Wait for settings to be applied
    assert dec(connection.read_until()) == "c[1,0,5]\n"
    # Set the FEC threshold to 30
    connection.write(enc("c[0,1,30]\n"))
    sleep(0.1) # Wait for settings to be applied
    assert dec(connection.read_until()) == "c[0,1,30]\n"
    return connection
   