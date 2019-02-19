# move mesh vertex x & y position to match the UV values for that vertex
from pymel.core import *

sel = PyNode('rounded_edge')
shape = listRelatives(sel)[0]
for i in range(len(shape.vtx)):
    vtx = shape.vtx[i]
    print("i = ", vtx)
    uv = vtx.getUVs('MainUV');
    print(uv)
    move(vtx, uv[0][0], uv[1][0], vtx.getPosition()[2])
