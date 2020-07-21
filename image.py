# Module to collect, store, and process images
import os
import arrow
import config

from ftplib import FTP, error_temp
from time import sleep
from io import BytesIO
from picamera import PiCamera


class ImageCollect:

    def __init__(self, year, month, day):

        self._create_cam()

        if config.Misc.archive_host == 'ftp':
            self._connect_ftp(year, month, day)

    def __del__(self):
        try:
            self._ftp.quit()
        except:
            pass

    def _create_cam(self):

        self._cam = PiCamera()
        self._cam.resolution = config.TLConfig.resolution
        self._cam.start_preview()
        sleep(3)
        self._start_preview_time = arrow.now().timestamp

    def _connect_ftp(self, year, month, day):

        self._ftp = FTP(config.FTPServerDetails.address)
        self._ftp.login(
            user=config.FTPServerDetails.username,
            passwd=config.FTPServerDetails.password
        )

        self._check_ftp_exists(year, month, day)
        self._change_ftp_cwd(year, month, day)

    def _check_ftp_exists(self, year, month, day):
        self._ftp.cwd(config.FTPServerDetails.location)

        try:
            file_list = self._ftp.nlst()
            if str(year) not in file_list:
                self._ftp.mkd(str(year))
        except error_temp as e:
            self._ftp.mkd(str(year))

        self._ftp.cwd(os.path.join(
            config.FTPServerDetails.location,
            str(year)
        ))

        try:
            file_list = self._ftp.nlst()
            if str(month) not in file_list:
                self._ftp.mkd(str(month))
        except error_temp as e:
            self._ftp.mkd(str(month))

        self._ftp.cwd(os.path.join(
            config.FTPServerDetails.location,
            str(year),
            str(month)
        ))

        try:
            file_list = self._ftp.nlst()
            if str(day) not in file_list:
                self._ftp.mkd(str(day))
        except error_temp as e:
            self._ftp.mkd(str(day))

        self._ftp.cwd(os.path.join(
            config.FTPServerDetails.location,
            str(year),
            str(month),
            str(day)
        ))

    def _change_ftp_cwd(self, year, month, day):

        self._ftp.cwd(os.path.join(
            config.FTPServerDetails.location,
            str(year),
            str(month),
            str(day)
        ))

    def _upload_to_ftp(self, stream, fn):

        self._ftp.storbinary('STOR %s' % fn, stream)

    def get_image(self, img_loc, img_time):

        fn = '%s.png' % str(img_time.timestamp)
        fn_full_path = os.path.join(img_loc, fn)

        if config.Misc.printing:
            print('Creating %s' % fn)

        if not config.Misc.testing:

            if config.Misc.archive_host == 'local':
                self._cam.capture(fn_full_path, format='png')

            if config.Misc.archive_host == 'ftp':
                stream = BytesIO()
                self._cam.capture(stream, format='png')
                stream.seek(0)
                self._upload_to_ftp(
                    stream,
                    fn
                )


if __name__ == '__main__':

    ic = ImageCollect(
        arrow.now().year,
        arrow.now().month,
        arrow.now().day
    )
    ic.get_image('/home/pi/', arrow.now())
