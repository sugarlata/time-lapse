import os
import main
import arrow
import datetime
import youtube_upload

ARCHIVE_LOCATION = main.ARCHIVE_LOCATION


def upload_to_youtube(days_back=1):
    # Check if file exists
    yestdy = arrow.now() - datetime.timedelta(days=days_back)
    loc = os.path.join(ARCHIVE_LOCATION, str(yestdy.year), str(yestdy.month), str(yestdy.day))
    dt = str(yestdy.format('YYYY-MM-DD'))
    mp4_fn = '.mp4' % dt

    vid_fn = os.path.join(loc, mp4_fn)

    if os.path.exists(vid_fn):
        sun_times = main.get_sun_times(yestdy)
        start_time = (sun_times['dawn'] - datetime.timedelta(minutes=10)).format('DD/MM/YYYY HH:mm')
        finish_time = (sun_times['dusk'] + datetime.timedelta(minutes=10)).format('DD/MM/YYYY HH:mm')
        resp = youtube_upload.upload(vid_fn, 'Doncaster Time Lapse %s' % dt, """Time lapse from Doncaster, Victoria, Australia.
Taken looking NW. 1 Frame / 3 seconds. 25fps.
Date: %s
Start time: %s
Finish time: %s""" % (dt, start_time.format('HH:mm'), finish_time.format('HH:mm')), '28', '', 'public')

        print resp
