import maya.cmds as mc
import maya.OpenMaya as om
from math import fmod

def rayIntersect(mesh, point, direction):

	#posted on cgtalk.com
	
	om.MGlobal.clearSelectionList()
	
	om.MGlobal.selectByName(mesh)
	sList = om.MSelectionList()
	#Assign current selection to the selection list object
	om.MGlobal.getActiveSelectionList(sList)
	
	item = om.MDagPath()
	sList.getDagPath(0, item)
	item.extendToShape()
	
	fnMesh = om.MFnMesh(item)
	
	raySource = om.MFloatPoint(point[0], point[1], point[2], 1.0)
	rayDir = om.MFloatVector(direction[0], direction[1], direction[2])
	faceIds = None
	triIds = None
	idsSorted = False
	testBothDirections = False
	worldSpace = om.MSpace.kWorld
	maxParam = 999999
	accelParams = None
	sortHits = True
	hitPoints = om.MFloatPointArray()
	#hitRayParams = om.MScriptUtil().asFloatPtr()
	hitRayParams = om.MFloatArray()
	hitFaces = om.MIntArray()
	hitTris = None
	hitBarys1 = None
	hitBarys2 = None
	tolerance = 0.0001
	hit = fnMesh.allIntersections(raySource, rayDir, faceIds, triIds, idsSorted, worldSpace, maxParam, testBothDirections, accelParams, sortHits, hitPoints, hitRayParams, hitFaces, hitTris, hitBarys1, hitBarys2, tolerance)
	
	result = int(fmod(len(hitFaces), 2))
	
	#clear selection as may cause problem if the function is called multiple times in succession
	om.MGlobal.clearSelectionList()
	return result


def parToLocMesh(mesh, particles):

	trinode = mc.polyTriangulate(mesh, ch = True)
	#count the particles
	count = mc.getAttr( particles + '.count' )
	#create a group for the locators
	locGroup = mc.group( em=True )
	newCount = 0	
	for p in range(count):
		pos = mc.getParticleAttr( ('%s.pt[%d]'%(particles, p)), at='worldPosition' )
		point = (pos[0] , pos[1] , pos[2])
		direction=(0.0, 1.0, 0.0)

		if rayIntersect(mesh, point , direction):
			loc = mc.spaceLocator( )
			mc.move( pos[0] , pos[1] , pos[2], loc, a = True )
			mc.scale( 0.1, 0.1, 0.1, loc, a = True, p = ( pos[0] , pos[1] , pos[2] ))
			mc.parent(loc, locGroup)
			newCount = newCount + 1
			
	locGroup = mc.rename(locGroup , 'loc_%d_GRP' % (newCount) )
	mc.delete (trinode)

	return locGroup


def particleToLocator(particles):
	#count the particles
	count = mc.getAttr( particles + '.count' )
	#create a group for the locators
	locGroup = mc.group( em=True, name='loc_%d_GRP' % (count) )
	for p in range(count):
		pos = mc.getParticleAttr( ('%s.pt[%d]'%(particles, p)), at='worldPosition' )
		loc = mc.spaceLocator( )
		mc.move( pos[0] , pos[1] , pos[2], loc, a = True )
		mc.scale( 0.1, 0.1, 0.1, loc, a = True, p = ( pos[0] , pos[1] , pos[2] ))
		mc.parent(loc, locGroup)
	return locGroup


def cubeCell(obj,parent,mat,aPos):
	mc.setAttr(obj + '.visibility', False)
	BB = mc.exactWorldBoundingBox(obj)
	activeShard = mc.polyCube( ch = False, sx=1, sy=1, sz=1, w = ((BB[3]-BB[0])*2), h=((BB[4]-BB[1])*2), d = ((BB[5]-BB[2])*2))
	activeShard = activeShard[0]
	mc.move(aPos[0], aPos[1], aPos[2], activeShard, a = True)
	mc.setAttr(activeShard + '.visibility', True)
	mc.sets( activeShard, forceElement = ('%sSG' % (mat)),  e = True)
	dupe = mc.duplicate(obj, rr = True)
	cutShard = dupe[0]
	mc.delete (cutShard, ch = True)
	mc.setAttr(cutShard + '.visibility', True)
	return activeShard, cutShard


def makeMat(obj, color):
	#create material if it doesn't exist
	mat =(obj + '_shardMat')
	exists = mc.objExists(mat)
	if ( exists == 0 ):
		mc.shadingNode( 'lambert', asShader = True, name = mat )
		mc.sets( renderable = True, noSurfaceShader = True, empty = True, name = (mat + 'SG'))
		mc.connectAttr( (mat + '.outColor'), (mat + 'SG.surfaceShader'), force = True)
		mc.setAttr((mat + '.color'), color[0], color[1], color[2], type = "double3") 
	return mat

		
def cutCell(obj, mat, pos, rot, shardsGRP):
	#do the cut procedure
	tocut = mc.polyEvaluate(obj, face = True)
	mc.polyCut( ('%s.f[0:%d]'% (obj,tocut)), pc = (pos[0], pos[1], pos[2]), ro = (rot[0], rot[1], rot[2]), ch = False, df = True)
	cutFaces = mc.polyEvaluate(obj, face = True)
	mc.polyCloseBorder(obj, ch = False)
	newFaces = mc.polyEvaluate(obj, face = True)
	newFaces = newFaces - cutFaces
	#assign material to faces
	for face in range(newFaces):
		mc.sets( ( '%s.f[ %d ]' % (obj, (cutFaces + newFaces - 1))), forceElement = ('%sSG' % (mat)),  e = True)


def calcMidPointMVector(posA, posB, aim, offset):
	midpoint = (posA + posB) /2
	dir = om.MVector.normal(posA - posB)
	offset = dir * offset
	offMidPoint = midpoint + offset
	rotate = mc.angleBetween( euler=True, v1=(aim[0], aim[1], aim[2]), v2=(dir.x, dir.y, dir.z) )
	cut = (offMidPoint, rotate)
	return cut


def locToPointMVector(group):
	points = []
	locators = mc.listRelatives ( group )
	for loc in locators:
		point = mc.xform(loc, q = True, ws = True, t = True)
		vector = om.MVector( point[0], point[1], point[2] )
		points.append(vector)
	return points


def bbMinMaxMVector(obj):

	#returns the vector values of the BB of an object
	objBB = mc.exactWorldBoundingBox(obj)
	objBBmin = om.MVector(objBB[0],objBB[1],objBB[2])
	objBBmax = om.MVector(objBB[3],objBB[4],objBB[5])
	centre = (objBBmin + objBBmax )/2
	outmin = objBBmin - centre
	outmax = objBBmax - centre
	
	return 	outmin, outmax
	#return  objBBmin,objBBmax


def arePointsInRad(radius, axis, points):
	# find if any of a list of points is within a radius of an axis
	inrad = []
	for point in points:
		mag = om.MVector.length(point - axis)
		if mag <= radius: inrad.append(point)
	return inrad


def findMaxDistance1(BBmin,BBmax,point):			
	#find the max distance a point can travel in a bounding box
	
	#produce second max diagonal
	min2 = om.MVector(BBmax.x, BBmax.y, BBmin.z)
	max2 = om.MVector(BBmin.x, BBmin.y, BBmax.z)
	
	#check the lengths
	tomin1 = om.MVector.length(point - BBmin)
	tomax1 = om.MVector.length(point - BBmax)
	tomin2 = om.MVector.length(point - min2)
	tomax2 = om.MVector.length(point - max2)
	
	if tomin1 > tomax1: len1 = tomin1
	else : len1 = tomax1
	if tomin2 > tomax2: len2 = tomin2
	else : len2 = tomax2
	
	if len1 > len2: return len1
	else: return len2# not used


def findMaxDistance(BBmin,BBmax,point):			
	#find the max distance a point can travel in a bounding box
	
	#produce eight points
	p1 = om.MVector(BBmin.x, BBmin.y, BBmin.z)
	p2 = om.MVector(BBmin.x, BBmax.y, BBmin.z)
	p3 = om.MVector(BBmax.x, BBmin.y, BBmin.z)
	p4 = om.MVector(BBmax.x, BBmax.y, BBmin.z)
	p5 = om.MVector(BBmin.x, BBmin.y, BBmax.z)
	p6 = om.MVector(BBmax.x, BBmin.y, BBmax.z)
	p7 = om.MVector(BBmin.x, BBmax.y, BBmax.z)
	p8 = om.MVector(BBmax.x, BBmax.y, BBmax.z)
	
	corners = p1,p2,p3,p4,p5,p6,p7,p8
	lengths = []
	
	for p in corners:
		len = om.MVector.length(point - p)
		lengths.append(len)
		
	lengths.sort(reverse=True)
	
	return lengths[0]

	
def makeMVectorBB(pos, BBmin, BBmax, factor):
	#make a 'bounding box' from a point and 2 vectors
	bbmin = BBmin * factor
	bbmax = BBmax * factor
	outmin = pos + bbmin
	outmax = pos + bbmax
	
	return outmin, outmax

	
def arePointsinBBMVector(BBmin, BBmax, points):
	inPoints =[]
	for point in points:
		if BBmin.x <= point.x <= BBmax.x:
			if BBmin.y <= point.y <= BBmax.y:
				if BBmin.z <= point.z <= BBmax.z :
					inPoints.append(point)
	return inPoints


def BBintersection1(BB1min, BB1max, BB2min, BB2max):
	#derive the bounding box that is the intersection of two bounding boxes
	#coords supplied and returned as MVector

	if BB1min.x >= BB2min.x: outMinX = BB1min.x
	if BB1min.x <= BB2min.x: outMinX = BB2min.x
	if BB1min.y >= BB2min.y: outMinY = BB1min.y
	if BB1min.y <= BB2min.y: outMinY = BB2min.y
	if BB1min.z >= BB2min.z: outMinZ = BB1min.z
	if BB1min.z <= BB2min.z: outMinZ = BB2min.z
	
	outMin = om.MVector(outMinX,outMinY,outMinZ)
	
	if BB1max.x <= BB2max.x: outMaxX = BB1max.x
	if BB1max.x >= BB2max.x: outMaxX = BB2max.x
	if BB1max.y <= BB2max.y: outMaxY = BB1max.y
	if BB1max.y >= BB2max.y: outMaxY = BB2max.y
	if BB1max.z <= BB2max.z: outMaxZ = BB1max.z
	if BB1max.z >= BB2max.z: outMaxZ = BB2max.z
	
	outMax = om.MVector(outMaxX,outMaxY,outMaxZ)
	
	return outMin,outMax#not used
	
	
def BBintersection(obj1, obj2):
	#derive the bounding box that is the intersection of two bounding boxes
	#coords returned as MVector
	
	BB1 = mc.exactWorldBoundingBox(obj1)
	BB2 = mc.exactWorldBoundingBox(obj2)
	
	BB1min = om.MVector(BB1[0],BB1[1],BB1[2])
	BB1max = om.MVector(BB1[3],BB1[4],BB1[5])

	BB2min = om.MVector(BB2[0],BB2[1],BB2[2])
	BB2max = om.MVector(BB2[3],BB2[4],BB2[5])	
	
	if BB1min.x >= BB2min.x: outMinX = BB1min.x
	if BB1min.x <= BB2min.x: outMinX = BB2min.x
	if BB1min.y >= BB2min.y: outMinY = BB1min.y
	if BB1min.y <= BB2min.y: outMinY = BB2min.y
	if BB1min.z >= BB2min.z: outMinZ = BB1min.z
	if BB1min.z <= BB2min.z: outMinZ = BB2min.z
	
	outMin = om.MVector(outMinX,outMinY,outMinZ)
	
	if BB1max.x <= BB2max.x: outMaxX = BB1max.x
	if BB1max.x >= BB2max.x: outMaxX = BB2max.x
	if BB1max.y <= BB2max.y: outMaxY = BB1max.y
	if BB1max.y >= BB2max.y: outMaxY = BB2max.y
	if BB1max.z <= BB2max.z: outMaxZ = BB1max.z
	if BB1max.z >= BB2max.z: outMaxZ = BB2max.z
	
	outMax = om.MVector(outMaxX,outMaxY,outMaxZ)
	
	return outMin,outMax


def delObjHistory(obj):
	mc.setAttr(obj + '.visibility', False)
	name = obj
	temp = mc.rename(obj, obj + '_orig')
	dupe = mc.duplicate(temp, rr = True, n = name)
	new_obj = dupe[0]
	mc.delete(new_obj, ch = True)
	return new_obj


def cubeVoro(obj, points, offset, rgb):
	mc.undoInfo( state = False)

	#variables
	usedPoints =[]
	validPoints =[]
	objBB = bbMinMaxMVector(obj)
	
	# open a progress window
	amount = 0
	mc.progressWindow(
	title = "Voronoi Shatter",
	progress = 0,
	status = "Initializing . . .",
	isInterruptable = True,
	maxValue = len(points)  )#end of progress window

	shardsGRP = mc.group(empty = True, name = (obj + '_shardsGRP'))
	color = rgb
	aim = (0,0,1) # Z_direction
	mat = makeMat(obj, color)
	check = 2*(om.MVector.length(objBB[1] - objBB[0]))
	


	for aPos in points:
	
		# Check if the dialog has been cancelled
		if mc.progressWindow( query=True, isCancelled=True ) : break
		# Check if end condition has been reached
		if mc.progressWindow( query=True, progress=True ) >= len(points) : break
		amount += 1
		
		#initialise the setup
		mult = 0.1
		BB1 = makeMVectorBB(aPos, objBB[0], objBB[1], mult)
		radius = om.MVector.length(objBB[1] - objBB[0])*2
		
		
		#initialise the lists
		usedPoints = [] # no used points here
		usedPoints.append(aPos)
		
		#dupe the cell
		shards = cubeCell(obj,shardsGRP,mat,aPos)
		activeShard = shards[0]
		#mc.delete(activeShard, ch = True)
		cutShard = shards[1]
		#mc.delete(cutShard, ch = True)
		
		while om.MVector.length(BB1[1] - BB1[0])< check:

			validPoints = []
			check1 = arePointsInRad(radius, aPos, points)
			check2 = arePointsinBBMVector(BB1[0], BB1[1], points)
			
			for point in check2:
				if point not in usedPoints and point in check1:
					validPoints.append(point)
				
			for bPos in validPoints:

				cutPos = calcMidPointMVector(aPos, bPos, aim, offset)
				cutCell(activeShard, mat, cutPos[0], cutPos[1], shardsGRP)
				usedPoints.append(bPos)
	
				#fit radius to activeShard, which will reduce with cuts
				#activeBB = bbMinMaxMVector(activeShard)
				intersect = BBintersection(activeShard, obj)
				radius = findMaxDistance(intersect[0], intersect[1], aPos)*2
				
			
			#increaseBB1 to get out of while loop
			mult *= 1.1
			BB1 = makeMVectorBB(aPos, objBB[0], objBB[1], mult)
			
		bool = mc.polyBoolOp( activeShard, cutShard, op=3, ch = False, n = (obj + '_shard_1'))
		#mc.delete(bool, ch = True)
		mc.parent(bool, shardsGRP)
		
		mc.progressWindow( edit=True, progress=amount, status=("Voronoi Shatter step %d of %d completed . . ." % (amount, len(points))) )
		mc.refresh()

	mc.progressWindow(endProgress=1)
	mc.undoInfo( state = True)

	
def doVoro(crack,rgb):
	#rgb = 1.0 , 1.0, 0.0
	#crack = 0.05
	sel = mc.ls( selection=True )
	points = locToPointMVector(sel[1])
	cubeVoro(sel[0], points, crack, rgb)
	
def doParToLoc():
	sel = mc.ls( selection=True )
	particleToLocator(sel[0])

def doConstParToLoc():
	sel = mc.ls( selection=True )
	parToLocMesh(sel[0], sel[1] )
