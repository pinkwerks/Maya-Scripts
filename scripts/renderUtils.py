# vim:ts=4:sw=4
#from pymel.core import *
import maya.cmds as mc
import maya.mel as mel

def disableImagePlane():
	objs = mc.ls(typ='imagePlane')
	for obj in objs:
		if not mc.editRenderLayerGlobals(q=1,crl=1) == 'defaultRenderLayer':
			mc.editRenderLayerAdjustment(obj+".displayMode")
		mc.setAttr(obj+".displayMode", 0)
		if not mc.editRenderLayerGlobals(q=1,crl=1) == 'defaultRenderLayer':
			mc.editRenderLayerAdjustment(obj+".type")
		mc.setAttr(obj+".type", 1)

def unsetBlackHoleForLayer():
        objs = mc.ls(sl=True)
        for obj in objs:
                mc.editRenderLayerAdjustment(obj+".matteOpacityMode");
                mc.setAttr(obj+".matteOpacityMode", 2)

def setBlackHoleForLayer():
        objs = mc.ls(sl=True)
        for obj in objs:
                mc.editRenderLayerAdjustment(obj+".matteOpacityMode");
                mc.setAttr(obj+".matteOpacityMode", 0)

def rms_caching():
        lights = mc.ls(typ='light')
        for light in lights:
                mc.setAttr(light+".caching", 1)
                mc.setAttr(light+".reuseDmap", 1)

def rms_caching_off():
        lights = mc.ls(typ='light')
        for light in lights:
                mc.setAttr(light+".caching", 1)
                mc.setAttr(light+".reuseDmap", 1)

def prepare_for_render():
        startShot()
        mc.setAttr('defaultRenderGlobals.imageFormat', 5)


def startShot():
        mc.setAttr('defaultRenderGlobals.imageFilePrefix', '<Scene>/<Scene>_<Layer>', type='string')
        mc.setAttr('defaultRenderGlobals.imageFilePrefix', lock=True)
        mc.setAttr('defaultRenderGlobals.animation', 1)
        mc.setAttr('defaultRenderGlobals.extensionPadding', 4)
        mc.setAttr('defaultRenderGlobals.enableDefaultLight', 0)
        mc.setAttr('defaultRenderGlobals.imageFormat', 5)
        mc.setAttr('defaultRenderGlobals.outFormatControl', 0)
        mc.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
        mc.setAttr('defaultRenderGlobals.periodInExt', 1)

# def hideImagePlanes():
#         mel.eval('warning("hideImagePlanes() : Ensuring image planes are hidden.")')
#         objs = mc.ls(typ='imagePlane')
#         for obj in objs:
#                 mc.setAttr(obj+".displayMode", 0)
#                 mc.setAttr(obj+".type", 1)

