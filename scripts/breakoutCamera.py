# setFGFilenameToFrame
# v20110314
# a premel script that switches up the 
# final gather final we a re rendering so we can stitch them together later

from pymel.core import *
import os
import maya.app.mentalray.renderProxyUtils
import maya.cmds as mc

def breakoutCamera():
    cams = []
    for i in selected():
        if i.getShape().type() == 'camera':
            cams.append(i.getShape())
    print '// breakoutCamera says, "Your selected cameras, Sir."'
    for cam in cams:
        newcam = duplicate(cam)[0]
        for a in newcam.listAttr():
            if a.isLocked():
                print a+' is locked'
                setAttr(a,lock=False)
        parent(newcam,w=1)
        newcam.scale.set([1,1,1])
        parentConstraint(cam.getParent(),newcam)

if __name__ == '__main__':
    breakoutCamera()
