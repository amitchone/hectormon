# Hectormon
A Raspberry Pi-based Flask webserver hosting an environmental control system for a Hermann's tortoise enclosure.


## Webserver
The webserver allows monitoring of basking temperature, non-basking temperature, basking and non-basking humidity, UV index output from the lamp, and a camera feed to allow for visual monitoring of the enclosure.

*Control* of the lamp is also possible, allowing remote switching.


## Sensing
Temperature and humidity is monitored via 2 separate **DHT22** temperature/humidity sensors.
UV Index is measured by a **UVM30A**.

All sensors are connected to an Arduino Uno which sends data via serial connection to the Raspberry Pi.


## Installation
1. `git clone https://github.com/amitchone/hectormon hectormon`
2. `cd hectormon/install`
3. `. setup.sh`
4. `sudo python app.py`

Note that the host IP address and port in `app.py, line 160` will more than likely need to be changed. It would also be wise to change the `secret_key`.
