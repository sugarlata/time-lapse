# Module to collect, store, and process images
import os
import arrow
import config


from time import sleep
from io import BytesIO
from picamera import PiCamera


class ImageCollect:

    def __init__(self):

        self._create_cam()

    def _create_cam(self):

        self._cam = PiCamera()
        self._cam.resolution = config.TLConfig.resolution
        self._cam.start_preview()
        sleep(3)
        self._start_preview_time = arrow.now().timestamp

    def get_image(self, img_loc, img_name):

        fn = os.path.join(img_loc, '%s.png' % img_name)

        if config.Misc.printing:
            print('Creating %s' % fn)

        if not config.Misc.testing:
            self._cam.capture(fn, format='png')


if __name__ == '__main__':

    ic = ImageCollect()
    ic.get_image('/home/pi/', 'test.png')
