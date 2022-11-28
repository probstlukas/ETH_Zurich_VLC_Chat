from sys import path
# adding shared folder to the system path
path.append('../shared')
from utility import default_port, serial_config  
from analyzer import Analyzer
from time import sleep

print("""
 _____  ______ _____  ______ ____  _____  __  __          _   _  _____ ______   __  __ ______           _____ _    _ _____  ______ __  __ ______ _   _ _______ 
|  __ \|  ____|  __ \|  ____/ __ \|  __ \|  \/  |   /\   | \ | |/ ____|  ____| |  \/  |  ____|   /\    / ____| |  | |  __ \|  ____|  \/  |  ____| \ | |__   __|
| |__) | |__  | |__) | |__ | |  | | |__) | \  / |  /  \  |  \| | |    | |__    | \  / | |__     /  \  | (___ | |  | | |__) | |__  | \  / | |__  |  \| |  | |   
|  ___/|  __| |  _  /|  __|| |  | |  _  /| |\/| | / /\ \ | . ` | |    |  __|   | |\/| |  __|   / /\ \  \___ \| |  | |  _  /|  __| | |\/| |  __| | . ` |  | |   
| |    | |____| | \ \| |   | |__| | | \ \| |  | |/ ____ \| |\  | |____| |____  | |  | | |____ / ____ \ ____) | |__| | | \ \| |____| |  | | |____| |\  |  | |   
|_|    |______|_|  \_\_|    \____/|_|  \_\_|  |_/_/    \_\_| \_|\_____|______| |_|  |_|______/_/    \_\_____/ \____/|_|  \_\______|_|  |_|______|_| \_|  |_|  

by Mélina Sladic & Lukas Probst.

Lets you measure the performance of VLC at different distances & find out the max range.\n
""")

### User input
DEFAULT_PORT = default_port()
DEFAULT_PAYLOAD_SIZE = 100 # in byte
DEFAULT_DISTANCE = 2 # in cm
DEFAULT_MEASUREMENT_TIME = 20 # in s

try:
    port = input(f"Enter the serial port to be used (default is {DEFAULT_PORT}): ") or DEFAULT_PORT
    is_measuring = input(f"Is this device used as a transmitter and does the measuring? ").strip().lower() == "yes"
    address = "AA" if is_measuring else "AB"

    if (is_measuring):
        payload_size = int(input(f"Enter the packet payload size to be used (default is {DEFAULT_PAYLOAD_SIZE} byte, max. is 200 byte): ").strip() or DEFAULT_PAYLOAD_SIZE)
        distance = int(input(f"Enter the distance of the LEDs in cm (default is {DEFAULT_DISTANCE} cm): ").strip() or DEFAULT_DISTANCE)
        measurement_time = int(input(f"Enter how long the measurement should  take at most in s (default is {DEFAULT_MEASUREMENT_TIME} s): ").strip() or DEFAULT_MEASUREMENT_TIME)

    print("Creating a serial connection to the transceiver...")
    serial = serial_config(port, address)
    print("Connected.\nMeasuring...")

    if (is_measuring):
        analyzer = Analyzer(serial, payload_size, distance, measurement_time)
        analyzer.measure()
        analyzer.save_results()
    else:
        print("Receiving measurements...")
        while True:
            serial.read_until()
            # A pause of around 10 milliseconds might be needed between each command, not to overload the microcontroller's interface
            sleep(0.01)
    # Writing the different exception class to catch/handle the exception
except EOFError:
        print('\nEOF exception, please enter something and try again.')
except KeyboardInterrupt:
        print('\nProgram terminated...')
