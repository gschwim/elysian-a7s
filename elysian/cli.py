import click
from cmd import Cmd
import glob
import os
from elysian import camera
from elysian import stacker

def setup():
    # setup for the run
    # We've got some stuff that takes time here - gphoto2/camera interaction can be, uh, slow
    # so let's be nice and show as progress bar.... :)
    # TODO - yeah, I'm lazy
    # TODO - is this even needed anymore? Should be handled in the 'image' subcommand

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



######### BEGIN WORKFLOWS ##########


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
    help="Directory that the stacked image will be output to. Defaults to --image-prefix.")
@click.option('--stack_prefix', '-sp',
    help="File prefix for the stacked images. Defaults to --image-prefix.")
def image(count, length, iso, img_prefix, no_init, stack, outdir, stack_prefix):
    """Automates bulb image captures using gphoto2 and libgphoto."""

    # setup for the run
    # We've got some stuff that takes time here - gphoto2/camera interaction can be, uh, slow
    # so let's be nice and show as progress bar.... :)

    click.echo('Setting things up. Standby....')

    #initialize a few things

    # the iterator for below
    iteration = 1  # we start at 1

    # set up for the live stack if that's what we're doing
    if stack:
        if not stack_prefix:
            stack_prefix = img_prefix
        if not outdir:
            outdir = img_prefix
        if not os.path.isdir(outdir):
            os.makedirs(outdir)

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
        img = '%s%d.arw' % (img_prefix, iteration)
        camera.capture(length, count, img_prefix, iteration)
        camera.mv_capture(img_prefix, iteration)
        if stack:
            stacker.stacker(img, iteration, outdir, stack_prefix)
        iteration = iteration + 1
    if stack:
        stacker.cleanup()

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
@click.option('--live', '-l', is_flag=True,
    help="Watch the present folder, stack live.")
@click.option('--outdir', '-od', required=True,
    help="Directory that the stacked image will be output to.")
@click.option('--stack_prefix', '-sp', default="stacked",
    help="Filename for the stacked image. Default is stack.tiff") # TODO - set a time/date filename to prevent overwriting
def stack(live, outdir, stack_prefix):
    """Folder will be stacked as images come in."""
    iteration = 1
    # check to see if outdir exists
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    if live:
        click.echo('SHIM - will watch and live stack the pwd.')
    else:
        imgList = glob.glob('*.arw')

    # get them stacked one by one
        for img in imgList:
            click.echo('Stacking %s' % img)
            stacker.stacker(img, iteration, outdir, stack_prefix)
            iteration = iteration + 1




