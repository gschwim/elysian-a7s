import click
from subprocess import call

from imager import camera

@click.group()
def cli():
    pass

##############
@cli.command()
@click.option('--count', '-c', type=int, default=1,
              help='Number of exposures to capture. Default is 1')
@click.option('--length', '-l', type=int, required=True,
              help='Length of exposure(s) in seconds.')
@click.option('--iso', '-i', type=int,
              help='ISO to be used. Default is to leave it unchanged.')
@click.option('--img-prefix', '-ip', default="capt",
              help='Prefix which image filenames will be based on. Default is "capt"')
def image(count, length, iso, img_prefix):
    """Automates bulb image captures using gphoto2 and libgphoto."""
    # basic housekeeping
    # get rid of any local capt0000.arw files
    call(['rm', 'capt0000.arw'])
    # the iterator for below
    iteration = 1  # we start at 1

    # init the camera
    camera.cam_init()
    # show the camera state
    present_iso = camera.cam_state()
    # set the camera as we'd like it
    camera.cam_setup(iso)
    # verify the camera state
    present_iso = camera.cam_state()
    # TODO pull the data display out of the cam_state() function
    # time to image

    click.echo('Subs: %dx%d seconds @ ISO%s' % (count, length, present_iso))
    while count >= iteration:
        # click.echo('Capturing image #:%d of %d' % (iteration, count))
        camera.capture(length, count, img_prefix, iteration)
        # mv_capture(img_prefix, iteration)
        iteration = iteration + 1
