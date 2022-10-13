#!/usr/bin/env python
import serial
#Testing - https://semfionetworks.com/blog/establish-a-console-connection-within-a-python-script-with-pyserial/

import serial
from time import sleep


def send_to_console(ser: serial.Serial, command: str, wait_time: float = 0.5):
    command_to_send = command + "\r"
    ser.write(command_to_send.encode('utf-8'))
    sleep(wait_time)
    print(ser.read(ser.inWaiting()).decode('utf-8'), end="")

with serial.Serial("/dev/tty.AirConsole-68-raw-serial", timeout=1) as ser:
    print(f"Connecting to {ser.name}...")
    send_to_console(ser, "")
    send_to_console(ser, "enable")
    send_to_console(ser, "show ap summary", wait_time=2)
    print(f"Connection to {ser.name} closed.")