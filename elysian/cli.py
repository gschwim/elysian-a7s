import click
from cmd import Cmd
from elysian import camera
from elysian import stacker

def setup():
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
@click.option('--stack', '-s', is_flag=True,
    help='Stack each image live as it comes in.')
@click.option('--outdir', '-od',
    help="Directory that the stacked image will be output to.")
@click.option('--outfile', '-of',
    help="Filename for the stacked image. Default is stack.tif") # TODO - set a time/date filename to pre
def image(count, length, iso, img_prefix, no_init, stack, outdir, outfile):
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
        camera.mv_capture(img_prefix, iteration)
        if stack:
            stacker.stacker(img_prefix, iteration)
        iteration = iteration + 1

@cli.command()
#@click.option('--capture', help="HELP!")
def shell():
    """Engages shell mode. This is good."""

    class shell(Cmd):
        ### TODO - shouldn't this be in a module?

        def __init__(self):
            Cmd.__init__(self)
            self.prompt = '-+>'
            self.intro = "Imager interactive CLI ready..."

        def do_help(self, args):
            if len(args) == 0:
                name = 'no args'
            else:
                name = args
            print "result is: %s" % name

        def do_quit(self, args):
            """Quits the session"""
            print "We're done..."
            return True

    ### Need to get things set up first!


    ### Call the class, start the console
    console = shell().cmdloop()

##############
@cli.command()
@click.option('--outdir', '-od', required=True,
    help="Directory that the stacked image will be output to.")
@click.option('--outfile', '-of',
    help="Filename for the stacked image. Default is stack.tif") # TODO - set a time/date filename to prevent overwriting
def stack():
    """Watched folder will be stacked as images come in."""
    pass

# TODO - also need to handle the files after written <--what did I mean by this?


