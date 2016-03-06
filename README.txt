elysian README

Author: Greg Schwimer - schwim <at><sign> bitrail*com

This python script started off with the intention of automating astronomical image capture
for the Sony A7* series cameras. In reality, it can be used for anything you wish
where 'bulb' type captures are required. It has since extended to live stacking
of the incoming images. It works precisely as well as I need it to, and I've gotten
a good number of fantastic images as a result.

BASICS

The elysian script is all command-line driven, and has a handful of top-level commands,
of which only the 'image' command presently does anything. The commands 'shell' and 'stack'
are shims for future capabilities.


CAMERA CONTROL

The A7* series of cameras have limited commercial software support. I have as of
yet been able to identify *any* software that can execute multiple (or any) bulb
captures of arbitrary length. The fine fellows at the libgphoto2/gphoto2 open-source
project for camera control were kind enough to put a quick fix into their code
that allows the A7* cameras to be operated in this way. 

The workflow for controlling the camera that is in this script is as simple as it
needs to be. Basically, we have the following:

	* Init the camera (this can be slow, use the '-ni' flag if the camera is already 
	connected to)
	* Read in the present settings, display them
	* Adjust to the desired settings, verify and display them (primarily -i for ISO,
	and enable 'bulb' mode.)
	* Begin the specified # of captures (-c):
		* Open the shutter
		* Wait '-l' seconds
		* Close the shutter and get the image file

LIVE STACKING

Live stacking is performed when the '-s' flag is enabled. The stacking method is very
rudimentary and is not meant for final image processing. The process is as follows:

	* Convert the incoming image to tiff. Debayer also done at this point w/ VNG.
	* Read the tiff file in as data, add to a numpy array
	* Divide the numpy array by the number of images in the array (average).
	* Output the array as a tiff image to './output/'

Testing has shown that good noise reduction is achieved, with a boost to SNR. YMMV.

EXAMPLE

The following execution will:

	* Set the camera ISO to 3200
	* Capture 30 subs of 300 seconds each
	* Stack the subs as they come in
	* NOT initialize the camera (only init once after camera power up, saves time!)

	elysian image -i 3200 -c 30 -l 300 -s -ni

Images are save to the present working directory, and stacked images are written to 
a subdirectory called 'output'.

QUIRKS

Simply put, I haven't programmed anything of interest in nearly 20 years, and certainly not
with python. So, this is a scratch effort and I'm learning on the fly. There are quirks, some
of which include:

	* Probably inefficient filesystem handling
	* Temp file cleanup does not happen if the script crashes
	* '-l' is an approximation. I've found that the actual exposure tends to be longer, which
	I've not considered a problem to date. For example, '-l 30' typically gets me a 36s exposure
	per the EXIF data in the resulting files. Longer exposures go higher in the delay. My gut
	tells me this is all camera-side or gphoto2 related.




