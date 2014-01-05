# makeBuffers.py
#
#  attempt to make auxillary buffers for selected object or materials
#  that are output to an EXR channel as compositing mattes.
#
# written with love by pink 2011-05-18
# arnold stuff added with mild enthusiasm by damon 2011-09-26
# more arnold stuff added under diress by pink 2011-09-28

from pymel.core import *
import maya.cmds as mc
import random

##
## predicates
##

def isMayaMaterial(mat):
    mats = set(["anisotropic",
                "blinn",
                "lambert",
                "layeredShader",
                "oceanShader",
                "phong",
                "phongE",
                "rampShader",
                "shadingMap",
                "surfaceShader",
                "useBackground"])
    if nodeType(mat) in mats:
        return True
    else:
        return False

def isMIMaterial(mat):
    mats = set(["mia_material",
                "mia_material_x",
                "mia_material_x_passes",
                "mib_illum_lambert",
                "mib_illum_phong",
                "mib_illum_blinn",
                "mib_illum_cooktorr",
                "mib_illum_ward",
                "mib_illum_ward_deriv",
                "mib_illum_hair",
                "dgs_material",
                "dielectric_material",
                "path_material",
                "mi_car_paint_phen",
                "mi_metallic_paint",
                "misss_call_shader",
                "misss_fast_shader",
                "misss_fast_simple_maya",
                "misss_fast_skin_maya",
                "misss_physical",
                "misss_skin_specular",
                "transmat"])
    if nodeType(mat) in mats:
        return True
    else:
        return False
		
def isArnoldMaterial(mat):
    mats = set(["aiAmbientOcclusion",
                "aiHair",
                "aiRaySwitch",
                "aiStandard",
                "aiUtility",
                "aiWireframe"
                # "aiWriteColor",
                # "aiWriteFloat"
                ])
				
    if nodeType(mat) in mats:
        return True
    else:
        return False

##
## maya general utils
##

def getShapeGeo(objs):
    geo = ls(objs,geometry=1)
    geo.extend(ls(listRelatives(selected(),s=1,ni=1),g=1))
    return geo

def mklist(obj):
    if isinstance(obj,list):
        return obj
    return list([obj])

def sg_for_geo(geos):
    sgs = []
    geos = mklist(geos)
    for geo in geos:
        for sg in listConnections(geo,type='shadingEngine'):
            sgs.append(sg)
    return sgs
    
def geo_for_sg(sgs):
    print('// geo_for_sg(')
    print(sgs)
    geos = []
    sgs = mklist(sgs)
    for sg in sgs:
        for geo in sets(sg, q=1):
            geos.append(geo)
    print('// geo_for_sg->')
    print(geos)
    return geos

def sg_for_mat(mat):
    sgs = []
    print('// sg_for_mat('+mat+')')
    sg = listConnections(mat+'.outColor')
    # xxx check if this is array
    if sg:
        if nodeType(sg[0]) == 'shadingEngine':
            sgs.append(sg[0])
    print('// sg_for_mat->')
    print(sgs)
    return sgs

def geo_for_mat(mat):
#    geos = []
#    for mat in mats:
    print('// geo_for_mat('+mat+')')
    sg = sg_for_mat(mat)
    geo = geo_for_sg(sg)
    print('// geo_for_mat:geo->')
    print(geo)
    return geo
#    geos.append(geo_for_sg(sg))


def materials_for_sg(sgs):
    renderer = getAttr('defaultRenderGlobals.currentRenderer')
    mats = []
    for sg in mklist(sgs):
        for shader in listConnections(sg+'.surfaceShader'):
            mats.append(shader)
        if renderer == 'mentalRay':
            mis = listConnections(sg.miMaterialShader)
            for mi in mis:
                mats.append(mi)
                ss = listConnections(sg.surfaceShader)
            for s in ss:
                mats.append(s)
    return mats

def materials_for_geo(geos):
    mats = []
    for geo in geos:
        mats.append(materials_for_sg(sg_for_geo(geo)))

def materials_only(objs):
    lst = filter(isMayaMaterial, objs)
    lst.extend(filter(isMIMaterial, objs))
    lst.extend(filter(isArnoldMaterial, objs))
    return lst

def create_material(name, material_type):
    '''Given a NAME and MATERIAL_TYPE, return the new material and shadingEngine.'''
    matname = name+'_'+material_type
    sgname = matname+'SG'
    sg = sets(renderable=True, noSurfaceShader=True, empty=True, name=sgname)
    mat_node = shadingNode(material_type, asShader=True, name=matname)
    connectAttr(mat_node+'.outColor', sg+'.surfaceShader')
    return (mat_node, sg)

##
## Arnold Utilities
##

def arnold_fast_settings():
    # disable lighting for matte passes here
#    setAttr "defaultArnoldRenderOptions.ignoreLights" 1
    return True

def arnold_disable_all_aovs(render_layers):
# arnold aovs aren't intergrated with renderlayers the same way as mentalray
    aovs = ls(type='aiAOV')
    for aov in aovs:
        try:
            print('// disabling aov = '+aov)
            editRenderLayerAdjustment(aov+'.enabled')
        except:
            print('// Couldn\'t set render layer override for AOV '+aov+'.')
        aov.setAttr('enabled',0)

def arnold_enable_aovs(render_layer, aovs):
    # arnold aovs aren't intergrated with renderlayers the same way as mentalray
    aovs = mklist(aovs)
    for aov in aovs:
        print('// enabling aov = '+aov)
        editRenderLayerAdjustment(aov+'.enabled',layer=render_layer)
        aov.setAttr('enabled',1)
    # else:
    #     print('// disabling aovs = '+aovs)
    #     editRenderLayerAdjustment(aovs+'.enabled',layer=render_layer)
    #     aovs.setAttr('enabled',1)

def printvar(name,vars):
    for v in mklist(vars):
        if isinstance(v,list):
            for i in v:
                print(name+'='+i)
        else:
            print(name+'='+v)

#
# The real work
#

def make_mr_pass(mats):
    renderPasses = []
    for mat in mats:
        matname = mat.replace(':','_') # fix namespace
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
	
def make_arnold_pass(mats):
    # make a render layer to store our modifications to
    # add all geometry connected to passed materials
    # if not mats:
    #     return
    # geos = []
    # for mat in mats:
    print('// make_arnold_pass:mats->')
    print(mats)
    #     sgs = listConnections(mat, type="shadingEngine")
    # #     geo = geo_for_mat(mat)
    # #     if geo:
    # #         geos.append(geo)
    # # print('// make_arnold_pass:geos->')
    # # print(geos)
    # # if geos:
    # geos = geo_for_sg(sgs)
    # rl = False
    # if geos:
    
    rl = False
#    rl = createRenderLayer(empty=1,name='MaterialMattes',nr=1,mc=1) # xxx this fucks up if shaders are not on masterBeauty
        
    setAttr('defaultArnoldRenderOptions.aovMode', 1)
    aovs = []
    for orig_mat in mats:
        matname = orig_mat.replace(':','_') # fix namespaceb
        # make the output AOV...
        # if we're getting a proxy surface shader from 'make_geo_layer()', strip "_shader" from the end.
        aov = createNode('aiAOV')
        aov = rename(aov,matname.rstrip('_shader')+'_matte')
        aovs.append(aov)
        aov.setAttr('name',matname.rstrip('_shader')+'_matte')
        
        #get the actual geo to which we will assign aiWriteColor
        SGs = listConnections(orig_mat, type="shadingEngine")
        geos = geo_for_sg(SGs)

        for index,geo in enumerate(geos):
            if index==0:
                # Only make a shadinggroup and material for the first geometry.
                # Since geos had the same material coming in, they should all get the same buffer
                wc_mat, wc_sg = create_material(orig_mat,'aiWriteColor') 
                setAttr(wc_mat.input,1,1,1)
                connectAttr(orig_mat+'.outColor', wc_mat+'.beauty', f=1)
                connectAttr(aov+'.name', wc_mat+'.aovName')
                connectAttr(aov+'.message', 'defaultArnoldRenderOptions.aovList', nextAvailable=1)
                select(geo)
                sets(wc_sg, forceElement=1)    # assign shader
                
    if rl:
        arnold_disable_all_aovs(rl) # disable all for render speed
        arnold_enable_aovs(rl, aovs) # turn on the ones we just created
    return aovs

def make_materials_layer(mats):
    renderer = getAttr('defaultRenderGlobals.currentRenderer')
    if renderer == 'arnold':
        make_arnold_pass(mats)
    elif renderer == 'mentalRay':
        make_mr_pass(mats)
    else:
        error('unsupported renderer '+renderer)

def make_geo_layer_old(geos):
    renderer = getAttr('defaultRenderGlobals.currentRenderer')
    if renderer == 'arnold':
        make_arnold_geo_layer(geos)
    elif renderer == 'mentalRay':
        make_mr_geo_layer(geos)
    else:
        error('unsupported renderer '+renderer)

def make_mr_geo_layer(geos):
    geos = mklist(geos)
    rl = createRenderLayer(geos,name='NameMe_Matte',nr=1,mc=1)
    # make surface shader for each geo
    for geo in geos:
        select(geo)
        mel.createAndAssignShader('surfaceShader','')
        # above command is crap and doesn't return anything usefull
        mat = materials_for_sg(listConnections(geo,type='shadingEngine'))[0]
        mat = rename(mat,geo+'_shader')
    mats = materials_for_geo(geos)
    passes = make_materials_layer(mats)
    # associate pass
    if getAttr('defaultRenderGlobals.currentRenderer') != 'arnold':
        for p in passes:
            rl.renderPass >> p.owner

def make_geo_layer(geos):
    if not geos:
        return False
    print('// make_geo_layer(geos)->')
    print(geos)
    geos = mklist(geos)
    # query user for input
    answer = mc.promptDialog(title='Sharc Question',
                             message='Enter name for new geomtry matte render layer.',
                             text='NameMe_Matte')
    print('// make_geo_layer:answer='+answer)
    if answer == 'dismiss':
        return False
    else:
        mc.promptDialog(q=1)
    # create a render layer to store our work in
    print('// make_geo_layer:geos->')
    print(geos)
    rl = createRenderLayer(geos,name=answer,nr=1,mc=1)
    print('// made render layer ='+rl+'\n')
    # make a SG, material, name it, color it
    sg = sets(renderable=1,noSurfaceShader=1,empty=1,name='geo_shader_SG')
    mat = shadingNode('surfaceShader',asShader=1)
    mat.outColor >> sg.surfaceShader
    mat = rename(mat,'geo_shader')
    mat.setAttr('outColorR',1)
    mat.setAttr('outColorG',1)
    mat.setAttr('outColorB',1)
    # assign new shader to the geos
    for geo in geos:
        sets(sg,forceElement=geo)
        arnold_disable_all_aovs(rl)
    return True

def main():
    s = selected()
    all_rndr_lyrs = listConnections('renderLayerManager.renderLayerId')
    if s:
        make_geo_layer(getShapeGeo(s))
        make_materials_layer(materials_only(s))
    else:
        mel.warning('Nothing to do. Select geometry or materials to make AOVs')
    select(s)

if __name__ == '__main__':
    main()
