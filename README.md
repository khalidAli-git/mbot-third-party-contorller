# mBot Linux Gamepad Controller

A lightweight Python and PlatformIO solution to control an mBot robot using a game controller's D-pad over a serial connection.

> **Platform Support:** This tool currently supports **Linux**. Windows support is planned for a future update.

---

## Features

* **Zero Heavy Dependencies:** Uses Python's native `evdev` library to talk directly to the Linux input subsystem, avoiding complex multimedia libraries like Pygame or SDL2.
* **Drift-Free Control:** Maps movement strictly to the controller's D-pad (HAT switches) rather than analog thumbsticks.
* **Auto-Reconnection Support:** Automatically handles controller disconnects and terminal interruptions cleanly.

---

## Prerequisites

Ensure you have the following installed on your Linux system:
* Python 3
* PlatformIO (VS Code Extension)
* A serial connection to your mBot

### Python Dependencies
Install the required Python packages using pip (preferably inside a virtual environment):

```bash
pip install pyserial evdev bleak

```

---

## Configuration

1. Open `controller.py` in your text editor.
2. Locate the port configuration near the top (around line 6):
```python
PORT = "/dev/mbot"

```


3. Update this path to match your mBot's actual serial port (e.g., `/dev/ttyUSB0`, `/dev/ttyACM0`, or `/dev/rfcomm0` if using an mBot Bluetooth module).

---

## Setup & Installation

### Step 1: Upload the Firmware

1. Connect your mBot to your PC or laptop via USB and make sure it is powered on.
2. Open your project folder in **VS Code**.
3. Ensure the **PlatformIO** extension is installed.
4. Build and upload the project code to your mBot.

### Step 2: Connect Your Controller

* Connect your game controller to your computer via a USB cable or pair it via **Bluetooth**.
* *(Note: If your mBot features a wireless Bluetooth module, you can run the robot entirely wirelessly without a USB tether from PC to robot).*

### Step 3: Run the Python Script

Run the controller script in your terminal:

```python
python3 controller.py

```

---

## Controls

* **D-Pad Up:** Move Forward (`F`)
* **D-Pad Down:** Move Backward (`B`)
* **D-Pad Left:** Turn Left (`L`)
* **D-Pad Right:** Turn Right (`R`)
* **Released:** Stop (`S`)

Press `Ctrl + C` in your terminal at any time to safely stop the mBot and exit the script
