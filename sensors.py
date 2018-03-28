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


def update_data():
    try:
        camera = picamera.PiCamera()
        remove('static/images/image.jpg')
    except:
        pass

    try:
        camera.capture('static/images/image.jpg')
        camera.close()
    except:
        pass

    try:
        del camera
    except:
        pass

    data = ser_read()

    if data:
        return {'ctemp': data[0], 'chum': data[1], 'htemp': data[2], 'hhum': data[3], 'uv': 7, 'parity': True}
    else:
        return {'ctemp': 'N/A', 'chum': 'N/A', 'htemp': 'N/A', 'hhum': 'N/A', 'uv': 'N/A', 'parity': False}


def temp_regex(temps):
    for temp in temps:
        regex = re.search("^(\d{2}[.]\d{2})$", temp)

        if regex is None:
            return False

    return True


def ser_read():
    ser = serial.Serial('/dev/ttyACM0', 9600)

    for i in range(5):
        data = ser.readline().split(',')
        data[-1] = data[-1][0:5]

        if len(data) == 4:
            if temp_regex(data):
                del ser
                return data

    return False
