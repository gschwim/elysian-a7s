from PIL import Image
import glob
import numpy as np
import time
import os
from subprocess import call

def rawdecode(img):
    call(['dcraw', '-o', '0', '-r', '1', '1', '1', '1', '-q', '1', '-t', '0', '-k', '0', '-H', '1', '-T', img])

def cal_flat(imgArray, mflat):
    pass


def OLDstacker(img_prefix, iteration):
    infile = '%s%d.arw' % (img_prefix,iteration)
    ppmfile = '%s%d.ppm' % (img_prefix,iteration)
    tifffile = '%s%d.tiff' % (img_prefix, iteration)
    # dcraw use:
    # -w = use in camera white balance
    # -g 2.4 12.92 - sRGB gamma curve applied
    # -o 2 sRGB color space
    # -q 1 use VNG interpolation
    # -t 0 do not flip the image based on orientation data in the exif
    #call(['dcraw', '-w', '-g', '2.4', '12.92', '-o', '2', '-q', '1', '-t', '0', infile])
    #call(['dcraw', '-W', '-g', '1', '1', '-o', '2', '-q', '1', '-t', '0', infile])
    # PixInsight Method - best to use tiff (lower SNR), -4 won't work with PIL, 8 bit output seems to be OK.
    call(['dcraw', '-o', '0', '-r', '1', '1', '1', '1', '-q', '1', '-t', '0', '-k', '0', '-H', '1', '-T', infile])



    if iteration == 1:
    	# create the array, save it for subsequent use
        imgArray = np.asarray(Image.open(tifffile))
        imgArray = imgArray.astype('uint32')
        np.save('nparray.npy', imgArray)
        # write out the first stacked image
        outImg = Image.fromarray(imgArray.astype('uint8'))
        outImg.save('./output/stacked_%s.tiff' % iteration)

        #clean up
        call(['rm', tifffile])
    else:
		#open the array image
        imgArray = np.load('nparray.npy')
		#open the new image to be added
        newImage = np.asarray(Image.open(tifffile))
        newImage = newImage.astype('uint32')

		#add the new image to the array and store the array
        imgArray = imgArray + newImage
        np.save('nparray.npy', imgArray)

		#average the stack by the number of iterations in the stack
        imgArray = imgArray/iteration

		#output the stacked image
        outImg = Image.fromarray(imgArray.astype('uint8'))
        outImg.save('./output/stacked_%s.tiff' % iteration)

        # clean up ppm files to save disk space
        call(['rm', tifffile])

def cleanup():
    call(['rm', 'nparray.npy'])

def stacker(img, iteration, outdir, stack_prefix, mflat):

    arrayName = '%s/%s.npy' % (outdir, stack_prefix)
    temptiff = '%s.tiff' % (img.split('.')[0])
    stackfile = '%s/%s_%s.tiff' % (outdir, stack_prefix, iteration)
    rawdecode(img)
    # check to see if stack is started, and if so, use it
    if not os.path.exists(arrayName):
        imgArray = np.asarray(Image.open(temptiff))
        imgArray = imgArray.astype('uint32')
        if mflat:
            cal_flat(imgArray, mflat)
        np.save(arrayName, imgArray)
        outImg = Image.fromarray(imgArray.astype('uint8'))
        outImg.save(stackfile)
        call(['rm', temptiff])
    else:
        #open the array
        imgArray = np.load(arrayName)

        #Open the image, prep to add to the array
        newImage = np.asarray(Image.open(temptiff))
        newImage = newImage.astype('uint32')

        # add the image to the array and save it
        imgArray = imgArray + newImage
        np.save(arrayName, imgArray)

        # average it
        imgArray = imgArray/iteration

        # write the stacked image
        outImg = Image.fromarray(imgArray.astype('uint8'))
        outImg.save(stackfile)

        #cleanup
        call(['rm', temptiff])





