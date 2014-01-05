import maya.mel as mel

frames=100
errorz=[]
for i in range(1,frames):
	try:
		mel.eval('file -import -type "OBJ" -prompt 0 -rpr "" "/jobs/josecuervo_cuervosilver/shots/bottle/houdini/geo/piece_.' + str(i) + '.obj";')
		print i
	except(RuntimeError):
		errorz.append(i)

if(len(errorz)>=1):
	print "these files had problems " + str(errorz)
else:
	print "done"

