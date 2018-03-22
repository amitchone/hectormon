import time


timestamp = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())


def Environmentals():
    environmentals = {
                        'ctemp': 25.6,
                        'htemp': 36.0,
                        'chum': 28.7,
                        'hhum': 18.5,
                        'uv': 8,
                        'timestamp': timestamp
                     }

    return environmentals
