import click
import subprocess
from subprocess import call
import time

LOGFILE = open('./logfile.log', 'w')

def cam_state():
    # Find settings like present ISO, shutterspeed, etc
    present_iso = subprocess.check_output(['gphoto2', '--get-config', 'iso']).splitlines()[2].split(':')[1].strip()
    present_shutterspeed = subprocess.check_output(['gphoto2',
                                                    '--get-config',
                                                    'shutterspeed']).splitlines()[2].split(':')[1].strip()
    click.echo('Camera presently at ISO: %s Shutter Speed: %s' % (present_iso, present_shutterspeed))
    return present_iso

def cam_setup(iso):
    # Set bulb mode and the iso requested
    call(['gphoto2', '--set-config', 'shutterspeed=Bulb'], stdout=LOGFILE, stderr=subprocess.STDOUT)
    if iso:
        call(['gphoto2', '--set-config', 'iso=%s' % iso], stdout=LOGFILE, stderr=subprocess.STDOUT)

def cam_init():
    # Initialize the camera. First, kill PTPCamera that always starts on OSX
    # because it won't let us bind to the port. Next, tell the camera we're here by
    # asking it some information about itself.
    # TODO - need error handling for these items
    # TODO - need an efficient way of redirecting the output of these. Maybe to a logfile?
    call(['killall', '-9', 'PTPCamera'], stdout=LOGFILE, stderr=subprocess.STDOUT)
    cam_init = call(['gphoto2', '--auto-detect', '--summary'], stdout=LOGFILE, stderr=subprocess.STDOUT)
    click.echo('Camera initialized')

def capture(length, count, img_prefix, iteration):
    # Triggers the capture by opening the shutter, waiting length time, then closing the shutter
    # and downloading the resultant file
    call(['gphoto2', '--set-config', 'bulb=1'], stdout=LOGFILE, stderr=subprocess.STDOUT)
    with click.progressbar(range(length*10), label='Capturing %s of %s:' % (iteration, count)) as bar:
        for x in bar:
            time.sleep(0.1)
        call(['gphoto2', '--set-config', 'bulb=0', '--wait-event-and-download=5s'],
             stdout=LOGFILE, stderr=subprocess.STDOUT)
        mv_capture(img_prefix, iteration)


def mv_capture(img_prefix, iteration):
    # click.echo('Captured as %s%d.arw' % (img_prefix, iteration))
    call(['mv', 'capt0000.arw', '%s%d.arw' % (img_prefix, iteration)])
