import asyncio
import evdev
from evdev import InputDevice, ecodes
from bleak import BleakClient

# mBot BLE module (Makeblock_LE). It is BLE-only: rfcomm / pyserial will NOT work.
MBOT_MAC = "1C:C8:C1:19:50:D4"
WRITE_UUID = "0000ffe3-0000-1000-8000-00805f9b34fb"   # mBot -> TX (write commands here)
NOTIFY_UUID = "0000ffe2-0000-1000-8000-00805f9b34fb"  # mBot -> RX (notifications)


def find_gamepad():
    for path in evdev.list_devices():
        dev = InputDevice(path)
        name = dev.name.lower()
        if "wireless controller" in name and "touchpad" not in name and "motion" not in name:
            return dev
    return None


async def main():
    gamepad = find_gamepad()
    if gamepad:
        print(f"Using gamepad: {gamepad.name} ({gamepad.path})")
    else:
        print("Wireless controller not found - will keep looking...")

    print(f"Connecting to mBot on {MBOT_MAC}...")
    client = BleakClient(MBOT_MAC, timeout=15.0)
    try:
        await client.connect()
        print("BLE connected!")

        async def on_notify(_characteristic, data):
            print(f"mBot: {data!r}", flush=True)

        try:
            await client.start_notify(NOTIFY_UUID, on_notify)
        except Exception:
            pass

        last_command = "S"
        print("Ready! Use the D-Pad to drive (Ctrl+C to stop).\n")
        try:
            while True:
                if gamepad is None:
                    gamepad = find_gamepad()
                    if gamepad is None:
                        print("Waiting for gamepad...", flush=True)
                        await asyncio.sleep(1)
                        continue
                    print(f"Using gamepad: {gamepad.name} ({gamepad.path})")

                try:
                    for event in gamepad.read_loop():
                        command = None
                        if event.type == ecodes.EV_ABS:
                            if event.code == ecodes.ABS_HAT0Y:
                                command = "F" if event.value < 0 else ("B" if event.value > 0 else "S")
                            elif event.code == ecodes.ABS_HAT0X:
                                command = "L" if event.value < 0 else ("R" if event.value > 0 else "S")

                        if command and command != last_command:
                            await client.write_gatt_char(WRITE_UUID, command.encode("utf-8"), response=True)
                            print(f"Drive Command: {command}", flush=True)
                            last_command = command
                except OSError as e:
                    print(f"Gamepad lost: {e} - reconnecting...", flush=True)
                    gamepad = None
        except KeyboardInterrupt:
            print("\nStopping mBot...")
            try:
                await client.write_gatt_char(WRITE_UUID, b"S", response=True)
            except Exception:
                pass
    finally:
        await client.disconnect()
        print("Disconnected.")


if __name__ == "__main__":
    asyncio.run(main())
