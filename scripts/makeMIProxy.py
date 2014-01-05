# makeMIProxy v20101117 by pink
#   make exporting and creating proxy geometry less painfull

from pymel.core import *
import os
import maya.app.mentalray.renderProxyUtils
import maya.cmds as mc

# XXX scene must be set to centimeters! something fucks up otherwise
# in mi translation - not this script's fault! fuckin maya....

def makeMIProxy(objs, outdir):
    mayafilename = os.path.basename(mc.file(q=1,sn=1)).split('.')[0]
    proxyObjs = list()

    for obj in objs:
        # make some names
        safe_long_name = obj.replace('|','_')
        miname = mayafilename+'-'+safe_long_name
        outnamepath = outdir[0]+'/'+miname+'.mi'

        # export the geo to mi with no shaders
        select(obj)
        mc.Mayatomr(
            binary=1,
            miStream=1,
            exportFilter=721600,
            active=1,
            fragmentExport=1,
            fis=1,
            fragmentChildDag=1,
            assembly=1,
            asn=miname,
            exportPathNames='n',
            file=outnamepath)

        # create a proxy cube and hook it up to the .mi
        proxyCube = polyCube(name=miname+'_makeMIProxy')
        proxyCube[0].getShapes()[0].setAttr('miProxyFile',outnamepath,type='string')
        select(proxyCube[0].getShapes()[0])
        maya.app.mentalray.renderProxyUtils.resizeToBoundingBox(mc.ls(sl=1)[0])
        proxyCube[0].getShapes()[0].setAttr('miUpdateProxyBoundingBoxMode',1)

        # force bounding box display of proxy even in shaded mode
        proxyCube[0].getShapes()[0].setAttr('overrideEnabled',1)
        proxyCube[0].getShapes()[0].setAttr('overrideLevelOfDetail',1)

        # get shader on original object and assign to proxy - this is money move
        select(obj)
        hyperShade(shaderNetworksSelectMaterialNodes=1)
        mat = ls(sl=1)
        select(proxyCube[0].getShapes()[0],add=1)
        hyperShade(assign=mat[0])

        # parent the proxy parallel to the the original geo
        select(obj)
        prt = pickWalk(d='up')
        select(proxyCube[0])
        select(prt,add=1)
        parent()

        # store the created proxy cubes
        proxyObjs.append(proxyCube[0])

    # finish up by organizing things
#    select(proxyObjs)
#    group(name='miproxy')
    select(objs)

def main():
    outdir = fileDialog2(cap='Select folder to store MI proxy',fm=3,okc='Select Folder')
    objs = ls(sl=1) 
    if len(objs):
        makeMIProxy(objs, outdir)

if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:expandtab

