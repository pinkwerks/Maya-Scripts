from pymel.core import *
import random

def randomColor():
    r = random.randrange(256) / 255.0
    g = random.randrange(256) / 255.0
    b = random.randrange(256) / 255.0
    a = random.randrange(256) / 255.0
    return (r,g,b,a)

def colorVertex(obj):
    """color verticies of a mesh example"""
    shape = selected()[0].getShapes()[0]
    print("shp=", shape)
    
    [shape.vtx[v].setColor(randomColor()) for v in shape.vtx.indicesIter()]

def main():
    objs=selected()
    [colorVertex(x) for x in objs]

if __name__ == '__main__':
    main()
