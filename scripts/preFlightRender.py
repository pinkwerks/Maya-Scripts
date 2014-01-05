# preFlight
# by pink 20111006
# attempt to rectify common mistakes before submitting a render

from pymel.core import *
import maya.cmds as mc
import maya.mel as mel

def disableImagePlane(rl):
    image_planes = mc.ls(typ='imagePlane')
    for ip in image_planes:
        if not rl == 'defaultRenderLayer':
            editRenderLayerAdjustment(ip+".displayMode",lyr=rl)
            editRenderLayerAdjustment(ip+".type",lyr=rl)
        mc.setAttr(ip+".displayMode", 0)
        mc.setAttr(ip+".type", 1)

def disableAllImagePlanes():
    all_rndr_lyrs = listConnections('renderLayerManager.renderLayerId')
    for rl in all_rndr_lyrs:
        disableImagePlane(rl)

# def resetCameraViews():
#     cams = ls(type='camera')
#     for cam in cams:
#         cam.setAttr("horizontalFilmOffset", 0)
#         cam.setAtrr(".verticalFilmOffset", 0)
#         cam.setAttr("overscan", 1)

def saneCommonRenderGlobals():
    shot = workspace.getPath().split('/')[6] # psyop specific!
    drg = ls(typ='renderGlobals')[0]
    if drg.getAttr('imageFilePrefix', lock=1):
        drg.setAttr('imageFilePrefix', lock=0)
    drg.setAttr('imageFilePrefix',
                'Incoming/<RenderLayer>_<RenderPass>/<Version>/'+shot+'_<RenderLayer>_<RenderPass>')
    drg.setAttr('animation',1)
    drg.setAttr('extensionPadding',4)
    drg.setAttr('enableDefaultLight',0)
    # these 2 have to be together
    drg.setAttr('imageFormat', 51) # exr
    drg.setAttr('imfPluginKey','exr')
    drg.setAttr('outFormatControl', 0)
    drg.setAttr('putFrameBeforeExt', 1)
    drg.setAttr('periodInExt', 1)

def saneArnoldRenderGlobals():
    ao = ls(typ='aiOptions')[0]
    ao.setAttr('driverHalfPrecision',1)
    ao.setAttr('log_console_verbosity',5)
    ao.setAttr('log_file_verbosity',5)
    ao.setAttr('aovMode',2)
    ao.setAttr('aovMode',1)
    ao.setAttr('texturePerFileStats',1)
    ao.setAttr('textureMaxMemoryMB',2048)
#    defaultArnoldRenderOptions.setAttr('textureAutomip',0)

def ensureRenderableCamera():
    cams = ls(type='camera')
    i = 0
    for cam in cams:
        if cam.getAttr('renderable'):
            i += 1
    if i == 0:
        error('No renderable cameras!')
    if i > 1:
        error('Too many renderable cameras!')

def main():
    saneCommonRenderGlobals()
    saneArnoldRenderGlobals()
    disableAllImagePlanes()
    ensureRenderableCamera()

if __name__ == '__main__':
    main()
