#!/bin/env python
# pink's poormans framecycler

import maya
import sys
import os
#import puke
import subprocess

if 'QBDIR' in os.environ:
    sys.path.append('%s/api/python' % os.environ['QBDIR']);
elif os.uname()[0] == 'Darwin':
    sys.path.append('/Applications/pfx/qube/api/python');
elif os.uname()[0] == 'Linux':
    sys.path.append('/usr/local/pfx/qube/api/python');
else:
    sys.path.append('c:/program files/pfx/qube/api/python');

# figure out which shot we're in based on the maya scene file name
def shotName():
	dir = maya.cmds.workspace(q=True,rd=1)
	p = dir.split('/')
	size = len(p)
	dir = p[size-3]
	print p
	return dir

def blastOff(*args):
	global window
	global destCtl
	dest=mc.textFieldGrp(destCtl,q=1,tx=1)
	mc.playblast(format='image',
		filename=shotName(),
		clearCache=1,
		viewer=1,
		showOrnaments=0,
		widthHeight=[2048,1168],
		fp=4,
		percent=100,
		)
		
#	mc.window(window,vis=0)

def buildGui():
#	global renderable_cameras
	global renderable_layers
	global layer_controls
	global window
	global rangeCtl
	global mrfmCtl
	global priorityCtl
	global destCtl

#	cam = renderable_cameras[0]

	window = mc.window(rtf=1,t='Blast-o-matic')
	form = mc.formLayout(nd=2)

#	label = 'Render frames '+fs+' to '+fe+' for '+cam+'?'
#	text = mc.text(l=label,fn='boldLabelFont')
#	mc.formLayout(form,edit=1,af=[text,'left',0])
#	mc.formLayout(form,edit=1,af=[text,'right',0])
#	mc.formLayout(form,edit=1,af=[text,'top',10])

	dir = maya.cmds.workspace(q=True,rd=1)
	destCtl = mc.textFieldGrp(l='Destination',tx=dir+'../images/renders/',ed=0,adj=2)
	mc.formLayout(form,edit=1,af=[destCtl,'top',5])
	mc.formLayout(form,edit=1,af=[destCtl,'left',0])
	mc.formLayout(form,edit=1,af=[destCtl,'right',5])

#	rangeCtl = mc.intFieldGrp(l='Cut Range',nf=2,v1=0,v2=0,ann='The number of shots before and after this one to include.',cc=rangeUpdate)
	rangeCtl = mc.intFieldGrp(l='Cut Range',nf=2,v1=0,v2=0,ann='The number of shots before and after this one to include.')
	mc.formLayout(form,edit=1,ac=[rangeCtl,'top',5,destCtl])
	mc.formLayout(form,edit=1,af=[rangeCtl,'left',0])
	mc.formLayout(form,edit=1,af=[rangeCtl,'right',0])

	priorityCtl = mc.radioButtonGrp(nrb=3,l='Priority',la3=['Low','Medium','High'],en=1,sl=2,vis=0)
	mc.formLayout(form,edit=1,ac=[priorityCtl,'top',5,rangeCtl])
	mc.formLayout(form,edit=1,af=[priorityCtl,'left',0])
	mc.formLayout(form,edit=1,af=[priorityCtl,'right',0])

#	groupCtl = mc.textFieldGrp(l='Groups',tx='mrfm',en=0,adj=2,m=0)
#	mc.formLayout(form,edit=1,ac=[groupCtl,'top',5,priorityCtl])
#	mc.formLayout(form,edit=1,af=[groupCtl,'left',0])
#	mc.formLayout(form,edit=1,af=[groupCtl,'right',0])

	clusterCtl = mc.textFieldGrp(l='Explicit Shot List',tx='',en=1,adj=2)
	mc.formLayout(form,edit=1,ac=[clusterCtl,'top',5,priorityCtl])
	mc.formLayout(form,edit=1,af=[clusterCtl,'left',0])
	mc.formLayout(form,edit=1,af=[clusterCtl,'right',0])

	audioCtl = mc.textFieldGrp(l='Audio File',tx=shotName(),en=1,adj=2)
	mc.formLayout(form,edit=1,ac=[audioCtl,'top',5,clusterCtl])
	mc.formLayout(form,edit=1,af=[audioCtl,'left',0])
	mc.formLayout(form,edit=1,af=[audioCtl,'right',0])

	submitBtn = mc.button(l='Blast Off!',c=blastOff)

	sep = mc.separator()
#	mc.formLayout(form,edit=1,ac=[sep,'top',5,lastCtl])
	mc.formLayout(form,edit=1,ac=[sep,'bottom',5, submitBtn])
	mc.formLayout(form,edit=1,af=[sep,'left',5])
	mc.formLayout(form,edit=1,af=[sep,'right',5])

	def killw(*args):
		mc.deleteUI(window,wnd=1)
	cancel = mc.button(l='Cancel',c=killw)

	mc.formLayout(form,edit=1,ap=[submitBtn,'left',5,1])
	mc.formLayout(form,edit=1,af=[submitBtn,'right',5])
#	mc.formLayout(form,edit=1,ac=[submitBtn,'top',5,sep])
	mc.formLayout(form,edit=1,af=[submitBtn,'bottom',5])

	mc.formLayout(form,edit=1,af=[cancel,'left',5])
	mc.formLayout(form,edit=1,ap=[cancel,'right',5,1])
#	mc.formLayout(form,edit=1,ac=[cancel,'top',5,sep])
	mc.formLayout(form,edit=1,af=[cancel,'bottom',5])

	mc.showWindow(window)
	pass
	
def main():
	buildGui()

if __name__ == '__main__':
	main()


