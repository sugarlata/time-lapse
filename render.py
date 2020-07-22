import os
import config
import arrow


def render_video(shift_yesterday=False):
    if shift_yesterday:
        yesterday = arrow.now().shift(days=-1)
    else:
        yesterday = arrow.now()
    
    vid_name = str(yesterday.format('YYYY-MM-DD'))
        
    os.chdir(os.path.join(
        config.Misc.archive_location,
        str(yesterday.year),
        str(yesterday.month),
        str(yesterday.day)))

    os.system(config.Misc.cmd % vid_name)


if __name__ == '__main__':

    render_video(shift_yesterday=True)