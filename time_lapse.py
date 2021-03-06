import os
import arrow
import config


from time import sleep
from utilities import get_sun_times, ensure_directory_is_valid
from image import ImageCollect
from cleanup import FTPMover


class TimeLapse:

    def __init__(self):

        self._vid_name = str(arrow.now().format('YYYY-MM-DD'))
        self._sun_times = get_sun_times()
        self._period = config.TLConfig.period

        self._year = arrow.now().year
        self._month = arrow.now().month
        self._day = arrow.now().day

        ensure_directory_is_valid(
            config.Misc.archive_location,
            str(self._year),
            str(self._month),
            str(self._day)
        )

        self._img_loc = os.path.join(config.Misc.archive_location, str(arrow.now().year), str(arrow.now().month), str(arrow.now().day))

    def start_blocking_loop(self):

        # Sleep until alloted time
        seconds_wait = (self._sun_times['dawn'] - 60 * config.TLConfig.minutes_before_dawn) - arrow.now().timestamp
        if seconds_wait > 0:
            sleep(seconds_wait)

        self._tl_loop()

        if config.Misc.archive_host == 'local':
            self._finish_loop()

    def _tl_loop(self):

        final_time = self._sun_times['dusk'] + 60 * config.TLConfig.minutes_after_sunset

        self._img_cap = ImageCollect(
            self._year,
            self._month,
            self._day
        )

        i = 0

        loop_start = arrow.now().timestamp
        while arrow.now().timestamp < final_time:

            wait_time = loop_start + (i * self._period) - arrow.now().timestamp

            if wait_time > 0:
                sleep(wait_time)

            try:
                self._img_cap.get_image(self._img_loc, arrow.now())
            except:
                pass

            if config.Misc.override:
                if i > config.Misc.override:
                    break

            i += 1

    def _finish_loop(self):

        os.chdir(self._img_loc)
        if config.Misc.printing:
            print(config.Misc.cmd % self._vid_name)

        os.system(config.Misc.cmd % self._vid_name)


