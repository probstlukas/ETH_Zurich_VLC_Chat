from sys import platform
from glob import glob

# Returns a default serial port based on the OS being used
def default_port():  
    # Windows
    if platform.startswith("win"):
        return "COM4"#may also be COM9 
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