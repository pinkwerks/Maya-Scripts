import os
import maya.cmds as mc

# set render globals > common > pre render frame
# python "execfile('/path/to/this/scripts/skipExisting.py')"


#def skipExisting():
dir = "/jobs/olay_2009/moisturizer/shots/olay15_001/images/renders"
root = "xxx"
ext = "rgb"
padsize = 4
frame = mc.currentTime(q=True)
format = "%0"+str(padsize)+"d"
framepad = format % frame # pad of 4, 3 would be '%03d'
image = dir+"/"+root+"."+framepad+"."+ext
if (os.path.isfile(image)):
	print "-------------------------------------"
	print "\n\n"+image+" exists! quitting.\n\n"
	print "-------------------------------------"
	mc.quit()
else:
	print "rendering "+image

