# Python 3 UDP LED server for Raspberry Pi and WS2821 LED-strips
This repository implements an UDP server for the Raspberry Pi and WS2821 LED-strips.
The client script also provides a music visualizer that uses `sounddevice` package and `numpy` to visualize audio data on the strip

[Video in action](https://streamable.com/vl59y)
(Song: Tiësto – BOOM)

## Configuration

### Hardware
You should be familiar with how to setup WS2821 LED-strip with your Pi, but in short

- Check the power consumption of the leds (mine are 0.3W when fully powered)
- Multiply that value with the amount of LEDs you're going to drive (0.3W * 120 = 36W)
- Make sure your power supply can handle it (the Pi wont be enough)
- The LED's take 5V, so the amperage that'll be going through at max power will be the consumption divided by 5 (36W / 5V = 7.2A)
- Make sure your wires will take the amperage, although this implementation probably won't drive the LEDs at max power anyways
- Connect the power supply
- Connect the Pi with the desired GPIO pin **AND** the ground pin!

### Server
This would be run on the Raspberry Pi

- Copy the `server.py` script on your Raspberry.
- Install the server requirements defined in `requirements.txt`
- Modify the script to configure the amount of pixels, GPIO pin, and the port of the server
- Run as sudo (for GPIO access)

### Client
This should be run on the device of which audio you want to visualize

- Install requirements defined in `requirements.txt`
- Modify the script to configure the amount of pixels, and the IP and port of the server
- Run it!

## Tested on
- Raspberry Pi 2B (server)
- Arch Linux with Python 3 and PulseAudio (client)
