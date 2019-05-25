import os
import arrow
import socket
import pysftp
import datetime

from io import BytesIO
from time import sleep
from astral import Location
from picamera import PiCamera
from config import ServerDetails


PRINTING = False
TESTING = False
OVERRIDE = None

# ARCHIVE_LOCATION = '/Volumes/SW/time-lapse'
ARCHIVE_LOCATION = '/media/nathan/Data/time-lapse'


def identify_hostname():
    return socket.gethostname()

def take_image(camera):
    stream = BytesIO()
    camera.capture(stream, format='jpeg')

    stream.seek(0)

    return stream

def upload_to_server(stream, fn):

    server_details = ServerDetails()

    with pysftp.Connection(server_details.address,
                           username=server_details.username,
                           password=server_details.password) as sftp:

        with sftp.cd(server_details.location):
            f = sftp.open('image.jpg', 'wb')
            f.write(stream.read())


if __name__ == '__main__':
    hostname = identify_hostname()
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(3)
    stream = take_image(camera)

    upload_to_server(stream, 'image.jpg')
