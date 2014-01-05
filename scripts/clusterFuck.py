import maya.cmds as mc

def clusterFuck(obj):
	grp = mc.spaceLocator()
	clusters = mc.listConnections(obj, type='skinCluster')
	for cluster in clusters:
		joints = mc.listConnections(cluster, type='joint')
		for joint in joints:
			joint = joint.replace(':', '__')
			mc.select(obj)
			dupe = mc.duplicate(rr=1, name=joint)
			mc.parent(world=True)
			mc.DeleteHistory()
			print grp
			mc.parent(dupe, grp)

if __name__ == '__main__':
	selected = mc.ls(sl=1, type='mesh')
#	print selected
	for s in selected:
		clusterFuck(s)

