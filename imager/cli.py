import click

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
@click.option('--no-init', '-ni', is_flag=True,
              help='Don\'t try to init the camera. Only use when the camera is already connected.')
def image(count, length, iso, img_prefix, no_init):
    """Automates bulb image captures using gphoto2 and libgphoto."""

    # setup for the run
    # We've got some stuff that takes time here - gphoto2/camera interaction can be, uh, slow
    # so let's be nice and show as progress bar.... :)
    # TODO - yeah, I'm lazy

    click.echo('Setting things up. Standby....')
    # the iterator for below
    iteration = 1  # we start at 1

    # init the camera
    if not no_init:
        camera.cam_init()

    # basic housekeeping
    camera.housekeeping()

    # show the camera state
    present_iso = camera.cam_state()

    # set the camera as we'd like it
    camera.cam_setup(iso)

    # verify the camera state
    present_iso = camera.cam_state()
    # time to image

    click.echo('Subs: %dx%d seconds @ ISO%s' % (count, length, present_iso))
    while count >= iteration:
        # click.echo('Capturing image #:%d of %d' % (iteration, count))
        camera.capture(length, count, img_prefix, iteration)
        # mv_capture(img_prefix, iteration)
        iteration = iteration + 1

# also need to handle the files after written
