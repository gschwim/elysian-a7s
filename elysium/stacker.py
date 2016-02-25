# dcraw -W -g 1 1 -o 2 -q 1 seems to work
# but we should correct white balance on the stack at the bottom of this script


from PIL import Image
import glob
import numpy as np
import time

def stacker():
	while(1):
		



imgList = glob.glob('./*.ppm')

first = True

for stacksize,img in enumerate(imgList):
	temp = np.asarray(Image.open(img))
	temp = temp.astype('uint32')

	print 'count: %s' % stacksize
	if first:
		sumImage = temp
		first = False
	else:
		sumImage = sumImage + temp

	#	avgArray = sumImage/len(imgList)
		print 'len is %s, stacksize is %s' % (len(imgList), stacksize)
		avgArray = sumImage/(stacksize + 1)
		avgImg = Image.fromarray(avgArray.astype('uint8'))
		avgImg.save('./output/output%s.tif' % stacksize)
		time.sleep(15)