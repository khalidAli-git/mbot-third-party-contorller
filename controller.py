import time
import serial
import evdev
from evdev import InputDevice, categorize, ecodes

PORT = "/dev/mbot"
BAUD = 9600

print(f"Connecting to mBot on {PORT}...")
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # Allow Arduino reset time
    print("Connected to mBot successfully!")
except Exception as e:
    print(f"Failed to connect to mBot: {e}")
    exit(1)

gamepad = None

# Locate the wireless controller device
devices = [InputDevice(path) for path in evdev.list_devices()]
for dev in devices:
    name_lower = dev.name.lower()
    if "wireless controller" in name_lower and "touchpad" not in name_lower and "motion" not in name_lower:
        gamepad = dev
        break

if not gamepad:
    print("\nNo controller found! Available devices:")
    for dev in devices:
        print(f" - {dev.name} ({dev.path})")
    exit(1)

print(f"\n-> Using controller: {gamepad.name} ({gamepad.path})")
print("Controller active! Use the D-Pad to drive. Press Ctrl+C to exit.")

last_command = 'S'

try:
    while True:
        try:
            for event in gamepad.read_loop():
                command = None
                
                # D-Pad on gamepads reports as an Absolute Axis (ABS_HAT0Y for vertical, ABS_HAT0X for horizontal)
                if event.type == ecodes.EV_ABS:
                    if event.code == ecodes.ABS_HAT0Y:
                        if event.value < 0:      # D-Pad Up
                            command = 'F'
                        elif event.value > 0:    # D-Pad Down
                            command = 'B'
                        else:
                            command = 'S'
                    elif event.code == ecodes.ABS_HAT0X:
                        if event.value < 0:      # D-Pad Left
                            command = 'L'
                        elif event.value > 0:    # D-Pad Right
                            command = 'R'
                        else:
                            command = 'S'

                if command and command != last_command:
                    ser.write(command.encode('utf-8'))
                    print(f"Sent command: {command}")
                    last_command = command
                    
        except OSError:
            print("\nController disconnected! Waiting for reconnection...")
            time.sleep(2)

except KeyboardInterrupt:
    print("\nExiting and stopping mBot...")
    ser.write(b'S')
    ser.close()
