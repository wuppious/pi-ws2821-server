#!/usr/bin/python3
import socket
from enum import Enum
from threading import Thread
import time
import board
import neopixel


PIXEL_COUNT = 60
PIXEL_SLEEP_TIME = 0.05
GPIO_PIN = board.D12

UDP_IP = '0.0.0.0'
UDP_PORT = 5000

# This is a global used for stopping the LED display thread
running_flag = True


class PixelThread(Thread):
    """Thread to update the led strip independent from the UDP listener"""

    def run(self):
        # having globals like this is bad practice, expecially with threading
        global running_flag, pixels
        while running_flag:
            pixels.show()
            time.sleep(PIXEL_SLEEP_TIME)


def update(data):
    """Update single led"""
    led = int.from_bytes(data[:2], 'big')  # 2 bytes for led position
    r, g, b = data[2:5]
    if led < PIXEL_COUNT:
        # any errors are caught by the caller
        pixels[led] = (r, g, b)


class Operation(Enum):
    """Reserve a few operation types"""
    START = 1
    STOP = 2
    UPDATE = 3


operation_data_length = {
    Operation.UPDATE.value: 5,
}

operations = {
    Operation.UPDATE.value: update,
}


def read(data):
    """Interpret operations from UDP packet data"""
    offset = 0
    while offset < len(data):
        operation = data[offset]  # 1 byte for operation type
        try:
            start = offset + 1
            length = operation_data_length[operation]
            end = start + length
            offset = end
            operation_data = data[start:end]
            operations[operation](operation_data)
        except Exception as e:
            print('Error:', e)
            pixels.fill((255, 0, 0,))  # blink leds in red to indicate error
            time.sleep(0.5)
            break


def main():
    global running_flag
    while running_flag:
        try:
            data, addr = sock.recvfrom(1024)
            read(data)
        except KeyboardInterrupt:
            running_flag = False
            pixels.deinit()
            exit()


# Initiate pixels, used globally
pixels = neopixel.NeoPixel(GPIO_PIN, PIXEL_COUNT, auto_write=False)
pixel_thread = PixelThread()
pixel_thread.start()


# Start listening for packets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

main()
