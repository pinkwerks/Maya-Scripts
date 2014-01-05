def colorVertex():
	"""color verticies of a mesh example"""
	shp = PyNode('pSphereShape1')
	[shp.vtx[v].setColor((v%10,1,0,1)) for v in shp.vtx.indicesIter()]
