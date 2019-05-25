import os
import arrow
import socket
import datetime

from ftplib import FTP
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

    sd = ServerDetails()

    ftp = FTP(sd.address)
    ftp.login(user=sd.username, passwd=sd.password)
    ftp.cwd(sd.location)
    ftp.storbinary('STOR image.jpg', stream)
    ftp.quit()
    

if __name__ == '__main__':
    hostname = identify_hostname()
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(3)
    stream = take_image(camera)

    upload_to_server(stream, 'image.jpg')
