# arnoldMakeMatteObject
#
# pink@pinkwerks.com
#
# select objects you want a 'hold out', 'matte' or 'black-hole'
# shader assigned to
#
# v20111207 - initial version

from pymel.core import *

def mklist(obj):
    '''Ensures OBJ is a list'''
    if isinstance(obj,list):
        return obj
    return list([obj])

def objectGeometry(objs):
    '''Given OBJECTS, return only geometry nodes.'''
    geo = ls(objs,geometry=1)
    geo.extend(ls(listRelatives(selected(),s=1,ni=1),g=1))
    return geo

def sg_for_geo(geos):
    '''Return a list of SGs (shadingEngines) for geometry'''
    sgs = []
    for geo in mklist(geos):
        connected = listConnections(geo,type='shadingEngine')
        if len(connected) < 1:
            mel.warning('arnoldMakeMatteObject: No shader attached to '+geo)
        for sg in connected:
            sgs.append(sg)
    return sgs

def materials_for_sg(sgs):
    '''Return a list of Materials for given SGs'''
    mats = []
    for sg in mklist(sgs):
#        mis = listConnections(sg.miMaterialShader)
#        for mi in mis:
#            mats.append(mi)
        mats.append(listConnections(sg.surfaceShader)[0])
    return mats

def materials_for_geo(geos):
    '''Return a list of Materials for given Geometry'''
    mats = materials_for_sg(sg_for_geo(geos))
    return mats

def create_material(name, material_type):
    '''Given a NAME and MATERIAL_TYPE, return the new material and shadingEngine.'''
    matname = name+'_'+material_type
    sgname = matname+'SG'
    sg = sets(renderable=True, noSurfaceShader=True, empty=True, name=sgname)
    mat_node = shadingNode(material_type, asShader=True, name=matname)
    connectAttr(mat_node+'.outColor', sg+'.surfaceShader')
    return (mat_node, sg)

def sg_for_mat(mat):
    '''Return a list of shadingEngines for a given material.'''
    connected = mklist(listConnections(mat+'.outColor'))
    sgs = []
    for thing in connected:
        if nodeType(thing) == 'shadingEngine':
            sgs.append(thing)
    return sgs

def material_displacement(material):
    '''Return the displacementShaders for the given material'''
    ds = []
    for sg in sg_for_mat(material):
        connection = connectionInfo(sg.displacementShader,sfd=1)
        if connection != '':
            #print('connection='+connection+'.')
            ds.append(connection)
    return ds

def make_holdout(objects):
    '''Given materials, create a matte or hold-out version of the material.'''
    for obj in mklist(objects):
        mats = materials_for_geo(obj)
        for mat in mklist(mats):
            safe_name = mat.replace(':','_') # fix namespace
            rayswitch, rssg = create_material(mat,'aiRaySwitch')
            mat.outColor >> rayswitch.shadow
            mat.outColor >> rayswitch.reflection
            mat.outColor >> rayswitch.refraction
            mat.outColor >> rayswitch.diffuse
            mat.outColor >> rayswitch.glossy
            setAttr(rayswitch.camera,0,0,0)
#            for sg in sg_for_mat(mat):
            disp_mat = material_displacement(mat)
            #print('disp_mat='+disp_mat+';')
            if disp_mat:
                if len(disp_mat) > 1:
                    mel.warning('arnoldMakeMatteObject: Found multiple displacementShaders - connecting '+disp_mat[0])
                print('disp_mat[0]='+disp_mat[0])
                print('rssg='+rssg)
                connectAttr(disp_mat[0], rssg+'.displacementShader')
                
            print('obj='+obj)
            select(obj)
            sets(rssg, forceElement=1)    # assign shader

def main():
    s = selected()
    if not s:
        mel.warning('arnoldMakeMatteObject : No objects selected to hold-out.')
        return
    make_holdout(objectGeometry(s))

if __name__ == '__main__':
    main()

