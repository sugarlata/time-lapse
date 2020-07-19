# Module to get the sunrise and sunset


def get_sun_times(dt=datetime.datetime.now()):

    loc = Location()
    loc.name = 'Melbourne'
    loc.region = 'Oceania'
    loc.latitude = -37.787027
    loc.longitude = 145.110013
    loc.timezone = 'Australia/Melbourne'
    loc.elevation = 75

    loc.solar_depression = 'civil'

    resp = {}
    for k, v in loc.sun(dt).items():

        resp[k] = arrow.get(v).timestamp

    return resp


def ensure_directory_valid(*args):

    base = ''
    for arg in args:
        base = os.path.join(base, arg)
        if not os.path.exists(base):
            os.mkdir(base)
    return True
