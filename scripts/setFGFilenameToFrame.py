# setFGFilenameToFrame
# 
# a premel script that switches up the 
# final gather final we a re rendering so we can stitch them together later

from pymel.core import *
import os
import maya.app.mentalray.renderProxyUtils
import maya.cmds as mc

def setFGFilenameToFrame():
    # make some easy to use names
    mayafilepath = mc.file(q=1,sn=1)
    scenedir = sceneName().parent
    mayafilename = os.path.basename(mc.file(q=1,sn=1)).split('.')[0]
    cf = '%04d' % int(mc.currentTime(q=1))
    #outfile = scenedir+'/'+mayafilename+'.'+cf+'.fgmap'
    outfile = mayafilename+'.'+cf+'.fgmap'
    #
    mrg = general.PyNode('mentalrayGlobals')
    mido = general.PyNode('miDefaultOptions')
#    mrg.setAttr('renderMode',3)
    mido.setAttr('finalGatherFilename',outfile,type='string')
    print('setFGFilenameToFrame() : '+outfile'\n')

if __name__ == '__main__':
    setFGFilenameToFrame()
