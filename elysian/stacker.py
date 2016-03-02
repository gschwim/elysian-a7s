# dcraw -W -g 1 1 -o 2 -q 1 seems to work
# but we should correct white balance on the stack at the bottom of this script


from PIL import Image
import glob
import numpy as np
import time
import os
from subprocess import call

def stacker(img_prefix, iteration):
    infile = '%s%d.arw' % (img_prefix,iteration)
    ppmfile = '%s%d.ppm' % (img_prefix,iteration)
    # dcraw use:
    # -w = use in camera white balance
    # -g 2.4 12.92 - sRGB gamma curve applied
    # -o 2 sRGB color space
    # -q 1 use VNG interpolation
    # -t 0 do not flip the image based on orientation data in the exif
    #call(['dcraw', '-w', '-g', '2.4', '12.92', '-o', '2', '-q', '1', '-t', '0', infile])
    call(['dcraw', '-W', '-g', '1', '1', '-o', '2', '-q', '1', '-t', '0', infile])


    if iteration == 1:
    	# create the array, save it for subsequent use
        imgArray = np.asarray(Image.open(ppmfile))
        imgArray = imgArray.astype('uint32')
        np.save('nparray.npy', imgArray)
        # write out the first stacked image
        outImg = Image.fromarray(imgArray.astype('uint8'))
        outImg.save('./output/stacked_%s.tif' % iteration)

        #clean up
        call(['rm', ppmfile])
    else:
		#open the array image
        imgArray = np.load('nparray.npy')
		#open the new image to be added
        newImage = np.asarray(Image.open(ppmfile))
        newImage = newImage.astype('uint32')

		#add the new image to the array and store the array
        imgArray = imgArray + newImage
        np.save('nparray.npy', imgArray)

		#average the stack by the number of iterations in the stack
        imgArray = imgArray/iteration

		#output the stacked image
        outImg = Image.fromarray(imgArray.astype('uint8'))
        outImg.save('./output/stacked_%s.tif' % iteration)

        # clean up ppm files to save disk space
        call(['rm', ppmfile])

def cleanup():
    call(['rm', 'nparray.npy'])


