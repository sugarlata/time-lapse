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

        if config.Misc.archive_host == 'ftp':
            self._connect_ftp()

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

    def _connect_ftp(self):
        
        self._ftp = FTP(config.FTPServerDetails.address)
        self._ftp.login(
            user=config.FTPServerDetails.username,
            passwd=config.FTPServerDetails.password
        )

    def check_ftp_exists(self, year, month, day):
        self._ftp.cwd(config.FTPServerDetails.archive_location)

        if str(year) not in self._ftp.nlst():
            self._ftp.mkd(str(year))
        self._ftp.cwd(os.path.join(
            config.FTPServerDetails.archive_location,
            str(year)
        ))

        if str(month) not in self._ftp.nlst():
            self._ftp.mkd(str(month))
        self._ftp.cwd(os.path.join(
            config.FTPServerDetails.archive_location,
            str(year),
            str(month)
        ))
        
        if str(day) not in self._ftp.nlst():
            self._ftp.mkd(str(day))
        self._ftp.cwd(os.path.join(
            config.FTPServerDetails.archive_location,
            str(day),
            str(month),
            str(day)
        ))

    def change_ftp_cwd(self, year, month, day):
        
        self._ftp.cwd(
            config.FTPServerDetails.archive_location,
            str(year),
            str(month),
            str(day)
        )

    def _upload_to_ftp(self, stream, fn, year, month, day):

        self._check_ftp_cwd(year, month, day)
        self._change_ftp_cwd(year, month, day)
        self._ftp.storbinary('STOR %s' % fn, stream)

    def get_image(self, img_loc, img_time):

        fn = os.path.join(img_loc, '%s.png' % str(img_time.timestamp))

        if config.Misc.printing:
            print('Creating %s' % fn)

        if not config.Misc.testing:

            if config.Misc.archive_host == 'local':
                self._cam.capture(fn, format='png')

            if config.Misc.archive_host == 'ftp':
                stream = BytesIO()
                self._cam.capture(stream, format='png')
                stream.seek(0)
                self._upload_to_ftp(
                    stream,
                    fn,
                    img_time.year,
                    img_time.month,
                    img_time.day
                )


if __name__ == '__main__':

    ic = ImageCollect()
    ic.get_image('/home/pi/', 'test.png')
