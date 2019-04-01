import os
import cv2
import arrow
import datetime

from time import sleep
from astral import Location


PRINTING = False
TESTING = False
OVERRIDE = None

# ARCHIVE_LOCATION = '/Volumes/SW/time-lapse'
ARCHIVE_LOCATION = '/media/nathan/Data/time-lapse'


def ensure_directory_valid(*args):

    base = ''
    for arg in args:
        base = os.path.join(base, arg)
        if not os.path.exists(base):
            os.mkdir(base)
    return True


def get_image(img_loc, img_name, cam):

    fn = os.path.join(img_loc, '%s.png' % img_name)
    if PRINTING:
        print 'Creating', fn

    if not TESTING:
        frame = cam.read()[1]
        cv2.imwrite(fn, frame)


def time_lapse_loop(img_loc, period, sun_times):

    final_time = sun_times['dusk'] + 60 * 10

    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    i = 0
    while arrow.now().timestamp < final_time:

        get_image(img_loc, str(arrow.now().timestamp), cam)

        if OVERRIDE:
            if i > OVERRIDE:
                break
            else:
                i += 1

        sleep(period)


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


def begin_day(period=3):

    vid_name = str(arrow.now().format('YYYY-MM-DD'))

    # Get sunrise / sunset
    sun_times = get_sun_times()

    # Sleep until 10 mins before dawn
    seconds_wait = (sun_times['dawn'] - 60 * 10) - arrow.now().timestamp
    if seconds_wait > 0:
        sleep(seconds_wait)

    # Create Filesystem
    ensure_directory_valid(ARCHIVE_LOCATION, str(arrow.now().year), str(arrow.now().month), str(arrow.now().day))
    img_loc = os.path.join(ARCHIVE_LOCATION, str(arrow.now().year), str(arrow.now().month), str(arrow.now().day))

    # Begin time lapse loop
    time_lapse_loop(img_loc, period, sun_times)

    # Combine into Video
    os.chdir(img_loc)
    if PRINTING:
        print """ffmpeg -y -pattern_type glob -i '*.png' -c:v libx264 -r 25 -crf 18 -pix_fmt yuv420p %s.mp4""" % vid_name

    os.system("""ffmpeg -y -pattern_type glob -i '*.png' -c:v libx264 -r 25 -crf 18 -pix_fmt yuv420p %s.mp4""" % vid_name)


if __name__ == '__main__':

    begin_day()
