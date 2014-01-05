# figure out which shot we're in based on the maya scene file name
def shotFromFilePath(fp):
	maya.cmds.workspace(q=True, sn=True)
	dir = fp
	p = fp.split('/')
	if (p[3] == 'shots' and p[5] == 'maya'):
		# /jobs/foo/foo_bar/shots/xxx000/maya
		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
	elif (p[3] == 'sequences' and p[6] == 'maya'):
		# /jobs/foo/foo_bar/sequences/xxx/xxx000/maya
		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]+'/'+p[5]
	elif (p[3] == 'assets' and p[5] == 'maya'):
		# /jobs/foo/foo_bar/assets/cunt/maya
		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
	elif (p[2] == 'shots' and p[4] == 'maya'):
		# /jobs/foo_bar/shots/xxx000/maya
		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]
	elif (p[2] == 'sequences' and p[5] == 'maya'):
		# /jobs/foo_bar/sequences/xxx/xxx000/maya
		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
	elif (p[2] == 'common' and p[5] == 'maya'):
		# /jobs/foo_bar/common/assets/cunt/maya
		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
	elif (p[2] == 'assets' and p[4] == 'maya'):
		# /jobs/foo_bar/assets/cunt/maya
		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]
	else:
		maya.mel.eval('warning("shotFromFilePath : Can\'t guess shot from supplied path! :")') 
	return dir

