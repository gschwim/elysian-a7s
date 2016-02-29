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
    call(['dcraw', '-W', '-g', '1', '1', '-o', '2', '-q', '1', infile])

    if iteration == 1:
    	# create the array
        imgArray = np.asarray(Image.open(ppmfile))
        imgArray = imgArray.astype('uint32')
        np.save('nparray.npy', imgArray)
        outImg = Image.fromarray(imgArray.astype('uint8'))
        outImg.save('./output/output%s.tif' % iteration)
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
        outImg.save('./output/output%s.tif' % iteration)

		



