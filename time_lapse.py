import arrow
import config


from time import sleep
from utilities import get_sun_times, ensure_directory_valid
from image import ImageCollect


class TimeLapse:

    def __init__(self):

        self._vid_name = str(arrow.now().format('YYYY-MM-DD'))
        self._sun_times = get_sun_times()
        self._period = config.TLConfig.period

        ensure_directory_is_valid(
            config.Misc.archive_location,
            str(arrow.now().year),
            str(arrow.now().month),
            str(arrow.now().day)
        )

        self._img_loc = os.path.join(ARCHIVE_LOCATION, str(arrow.now().year), str(arrow.now().month), str(arrow.now().day))

    def start_blocking_loop(self):

        # Sleep until alloted time
        seconds_wait = (sun_times['dawn'] - 60 * config.TLConfig.minutes_before_dawn) - arrow.now().timestamp
        if seconds_wait > 0:
            sleep(seconds_wait)

        self._tl_loop()
        self._finish_loop()

    def _tl_loop(self):

        final_time = self._sun_times['dusk'] + 60 * config.TLConfig.minutes_after_sunset

        self._img_cap = ImageCollect()

        i = 0

        while arrow.now().timestamp < final_time:

            self._img_cap.get_image(self._img_loc, str(arrow.now().timestamp))
        
            if config.TLConfig.override:
                if i > config.TLConfig.override:
                    break
                else:
                    i += 1

            sleep(self._period)
                
    def _finish_loop(self):

        os.chdir(self._img_loc)
        if config.TLConfig.printing:
            print(config.Misc.cmd % self._video_name)

        os.system(config.Misc.cmd % self._video_name)
