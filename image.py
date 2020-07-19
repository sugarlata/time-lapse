# Module to collect, store, and process images
import os
import cv2
import config

class ImageCollect(Object):

    def __init__(self):

        self._create_cam()

    def _create_cam(self):

        self._cam = cv2.VideoCapture
        self._cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self._cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)        

    def get_image(self, img_loc, img_name):

        fn = os.path.join(img_loc, '%s.png' % img_name)

        if config.Misc.printing:
            print('Creating', fn)

        if not config.Misc.testing:
            frame = self._cam.read()[1]
            cv2.imwrite(fn, frame)
