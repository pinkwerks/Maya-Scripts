# create a material for all selected things
# 2011-10-08

from pymel.core import *
import random

def mklist(obj):
    if isinstance(obj,list):
        return obj
    return list([obj])

def randomColor():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r,g,b)

def createSGWithMaterial(name, material_type):
    sg = sets(renderable=True, noSurfaceShader=True, empty=True, name=name + 'SG')
    mat = shadingNode(material_type, asShader=True, name=name )
    random_color = randomColor()
    if material_type != 'aiStandard':
        mat.setColor(random_color)
    else:
        mat.setAttr('KdColorR',random_color[0])
        mat.setAttr('KdColorR',random_color[1])
        mat.setAttr('KdColorR',random_color[2])
    mat.outColor >> sg.surfaceShader
    return sg

def createAndAssignMaterial(name, type, objs):
    objs = mklist(objs)
    mats = []
    for obj in objs:
        mat_sg = createSGWithMaterial(name, type)
        select(obj)
        sets(mat_sg, forceElement=1)
        mats.append(mat_sg)
    return mats

def shapesOnly(objs):
    geo = ls(objs,geometry=1)
    geo.extend(ls(listRelatives(selected(),s=1,ni=1),g=1))
    return geo

def main(materialType):
    things = shapesOnly(selected())
    for thing in things:
        createAndAssignMaterial(thing.name(), materialType, thing)

if __name__ == '__main__':
    main()

