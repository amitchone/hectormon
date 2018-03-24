import picamera, time, serial, re
from energenie import switch_on, switch_off
from os import remove


def toggle_lamp_on():
    try:
        switch_on(1)
        return True
    except:
        return False


def toggle_lamp_off():
    try:
        switch_off(1)
        return True
    except:
        return False


def picture():
    try:
        remove('static/images/image.jpg')
    except:
        pass

    camera = picamera.PiCamera()
    camera.capture('static/images/image.jpg')
    camera.close()
    del camera


def update_data():
    try:
        remove('static/images/image.jpg')
    except:
        pass

    camera = picamera.PiCamera()
    camera.capture('static/images/image.jpg')
    camera.close()
    del camera

    data = ser_read()

    if data:
        return {'ctemp': data[0], 'chum': data[1], 'htemp': data[2], 'hhum': data[3], 'uv': 7, 'parity': True}
    else:
        return {'ctemp': 'N/A', 'chum': 'N/A', 'htemp': 'N/A', 'hhum': 'N/A', 'uv': 'N/A', 'parity': False}


def temp_regex(temps):
    for temp in temps:
        regex = re.search("\A\d{2}[.]\d{2}\\b", temp)

        if regex is None:
            return False

    return True


def ser_read():
    ser = serial.Serial('/dev/ttyACM0', 9600)

    for i in range(5):
        data = ser.readline().split(',')

        if len(data) == 4:
            if temp_regex(data):
                del ser
                return data

    return False
