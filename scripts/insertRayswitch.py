# insertRayswitch.py
#
#  put a mib_rayswitch_advanced between a material and it's SG
#  and hook up the default behavior.
#
# written with love by pink 2011-05-25

from pymel.core import *
import random

def sg_for_material(material):
    sgs = []
    destinations = connectionInfo(texture.outColor,dfs=1)
    for d in destinations:
        sgs.append(d)
    return sgs

def insert(materials):
    raySwitches = []
    for mat in mats:
        for sg in sg_for_material(mat)
            matname = mat.replace(':','_') # fix namespace
            rs = createNode('mip_rayswitch_advanced',n='rayswitch_'+matname)
            mat.outColor >> rs.default
            rs.message >> sg.miMaterialShader
            rs.message >> sg.miShadowShader

        cb = createNode('writeToColorBuffer',n=matname+'_writeToColorBuffer')
        cb.color.set([1,1,1])
        rp = createNode('renderPass')
        rp = rename(rp,'matte_'+matname)
        rp.numChannels.set(1)
        rp.frameBufferType.set(256)
        setRenderPassType(rp,type="CSTCOL")
        mat.message >> cb.evaluationPassThrough
        rp.message >> cb.renderPass
        renderPasses.append(rp)
    return renderPasses

def main():
    selected_materials = ls(sl=1,mat=1)
    return insert(selected_materials)

if __name__ == '__main__':
    main()
