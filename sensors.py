import picamera, time, serial
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


def arduino_read():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    print ser.readline()


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
    return {'ctemp': data[0], 'chum': data[1], 'htemp': data[2], 'hhum': data[3], 'uv': 7}


def ser_read():
    ser = serial.Serial('/dev/ttyACM0', 9600)

    while True:
        data = ser.readline().split(',')

        if len(data) == 4:
            del ser
            return data
