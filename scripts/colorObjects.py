# colorObjects v20111117 by pink

from pymel.core import *
import random

def randomColors(objs):
    polyColorSet(create=1,clamped=0,rpt='RGBA',colorSet='random')
    for obj in objs:
        r=random.random()
        g=random.random()
        b=random.random()
        polyColorPerVertex(obj,r=r,g=g,b=b,a=1,cdo=1)

def randomAlphas(objs):
    for obj in objs:
        a=random.random()
        polyColorPerVertex(obj,a=1,cdo=1)

def makeConnections(objs):
    mrvtxc=createNode('mentalrayVertexColors')
    for n,obj in enumerate(objs):
        obj.getShape().colorSet[0].colorName >> mrvtxc.cpvSets[n]
 #       print obj.getShape().colorSet[0].colorName
        print obj.getShape().colorSet[0].colorName+" >> "+mrvtxc.cpvSets[n]
    print '// Connected '+str(n+1)+' objects to '+mrvtxc

def main():
    objs=selected()
    randomColors(objs)
    makeConnections(objs)

if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:expandtab

