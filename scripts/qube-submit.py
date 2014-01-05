#!/bin/env python
# submit a mentalray job to qube
# crafted with love by pink

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

import qb
format = "1280 720 0 0 1280 720 1 HD_720"
renderable_cameras = list()
renderable_layers = list()
layer_controls = list()
window = str()
renderer = mc.getAttr('defaultRenderGlobals.currentRenderer')

if renderer == "vray":
	fs = int(mc.getAttr('vraySettings.startFrame'))
	fe = int(mc.getAttr('vraySettings.endFrame'))
else:
	fs = int(mc.getAttr('defaultRenderGlobals.startFrame'))
	fe = int(mc.getAttr('defaultRenderGlobals.endFrame'))

# figure out which shot we're in based on the maya scene file name
def shotName():
	dir = maya.cmds.workspace(q=True,rd=1)
	p = dir.split('/')
	size = len(p)
	dir = p[size-2]
#	if (p[3] == 'shots' and p[5] == 'maya'):
		# /jobs/foo/foo_bar/shots/xxx000/maya
#		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
#	elif (p[3] == 'sequences' and p[6] == 'maya'):
		# /jobs/foo/foo_bar/sequences/xxx/xxx000/maya
#		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]+'/'+p[5]
#	elif (p[3] == 'assets' and p[5] == 'maya'):
		# /jobs/foo/foo_bar/assets/cunt/maya
#		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
#	elif (p[2] == 'shots' and p[4] == 'maya'):
		# /jobs/foo_bar/shots/xxx000/maya
#		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]
#	elif (p[2] == 'sequences' and p[5] == 'maya'):
		# /jobs/foo_bar/sequences/xxx/xxx000/maya
#		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
#	elif (p[2] == 'common' and p[5] == 'maya'):
		# /jobs/foo_bar/common/assets/cunt/maya
#		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]+'/'+p[4]
#	elif (p[2] == 'assets' and p[4] == 'maya'):
		# /jobs/foo_bar/assets/cunt/maya
#		dir = '/'+p[0]+'/'+p[1]+'/'+p[2]+'/'+p[3]
#	else:
#		maya.mel.eval('warning("shotName: Can\'t guess shot from supplied path! :")') 
	
	return dir

def check_renderable_cameras():
	global renderable_cameras
	cams = mc.ls(type='camera')
	numrcams = 0
	rcams = list()
	for cam in cams:
		if (mc.getAttr(cam+'.renderable')):
			numrcams += 1
			renderable_cameras.append(cam)
	if (numrcams != 1):
		answer = mc.confirmDialog(title='Confirm renderable cameras', message='Multiple renderable cameras exist, proceed?', button=['Yes','No'], defaultButton='Yes')	
		if (answer == 'No'):
			return 1
	return 0

def rangeUpdate(*args):
	global rangeCtl
	fs = mc.intFieldGrp(rangeCtl,q=1,v1=1)
	fe = mc.intFieldGrp(rangeCtl,q=1,v2=1)
#	mc.setAttr('defaultRenderGlobals.startFrame',fs)
#	mc.setAttr('defaultRenderGlobals.endFrame',fe)
	pass

def confirmRender():
	global renderable_cameras
	global renderable_layers
	global layer_controls
	global window
	global rangeCtl
	global mrfmCtl
	global priorityCtl
	global cpuReserveCtl
	global timeCtl; 

	cam = renderable_cameras[0]
#	scale = mc.xform(cam,q=1,s=1,ws=1)
#	if scale[0] != 1 and scale[1] != 1 and scale[2] != 1:
#		maya.mel.eval('warning("Camera scale is not 1 in world space!")')

	window = mc.window(rtf=1,t='Confirm Qube Submission')
	form = mc.formLayout(nd=2)

#	label = 'Render frames '+fs+' to '+fe+' for '+cam+'?'
#	text = mc.text(l=label,fn='boldLabelFont')
#	mc.formLayout(form,edit=1,af=[text,'left',0])
#	mc.formLayout(form,edit=1,af=[text,'right',0])
#	mc.formLayout(form,edit=1,af=[text,'top',10])

	camCtl = mc.textFieldGrp(l='Camera',tx=cam,ed=0,adj=2)
	mc.formLayout(form,edit=1,af=[camCtl,'top',5])
	mc.formLayout(form,edit=1,af=[camCtl,'left',0])
	mc.formLayout(form,edit=1,af=[camCtl,'right',5])

	rangeCtl = mc.intFieldGrp(l='Frame Range',nf=2,v1=int(fs),v2=int(fe),cc=rangeUpdate)
	mc.formLayout(form,edit=1,ac=[rangeCtl,'top',5,camCtl])
	mc.formLayout(form,edit=1,af=[rangeCtl,'left',0])
	mc.formLayout(form,edit=1,af=[rangeCtl,'right',0])

	sep_top2 = mc.separator()
	mc.formLayout(form,edit=1,ac=[sep_top2,'top',5,rangeCtl])
	mc.formLayout(form,edit=1,af=[sep_top2,'left',5])
	mc.formLayout(form,edit=1,af=[sep_top2,'right',5])

	priorityCtl = mc.radioButtonGrp(nrb=3,l='Priority',la3=['Low','Medium','High'],en=1,sl=2)
	mc.formLayout(form,edit=1,ac=[priorityCtl,'top',5,sep_top2])
	mc.formLayout(form,edit=1,af=[priorityCtl,'left',0])
	mc.formLayout(form,edit=1,af=[priorityCtl,'right',0])

	cpuReserveCtl = mc.intSliderGrp(l="Reserve Processors",f=1,v=8,min=0,max=16,fmn=0,fmx=16,adj=3)
	mc.formLayout(form,edit=1,ac=[cpuReserveCtl,'top',5,priorityCtl])
	mc.formLayout(form,edit=1,af=[cpuReserveCtl,'left',0])
	mc.formLayout(form,edit=1,af=[cpuReserveCtl,'right',0])

#	groupCtl = mc.textFieldGrp(l='Groups',tx='mrfm',en=0,adj=2,m=0)
#	mc.formLayout(form,edit=1,ac=[groupCtl,'top',5,priorityCtl])
#	mc.formLayout(form,edit=1,af=[groupCtl,'left',0])
#	mc.formLayout(form,edit=1,af=[groupCtl,'right',0])

	timeCtl = mc.intFieldGrp(l='Time Limit',nf=1,v1=45)
	mc.formLayout(form,edit=1,ac=[timeCtl,'top',5,cpuReserveCtl])
	mc.formLayout(form,edit=1,af=[timeCtl,'left',0])
	mc.formLayout(form,edit=1,af=[timeCtl,'right',0])

	clusterCtl = mc.textFieldGrp(l='Cluster',tx='/',en=1,adj=2)
	mc.formLayout(form,edit=1,ac=[clusterCtl,'top',5,timeCtl])
	mc.formLayout(form,edit=1,af=[clusterCtl,'left',0])
	mc.formLayout(form,edit=1,af=[clusterCtl,'right',0])

	sep_top3 = mc.separator()
	mc.formLayout(form,edit=1,ac=[sep_top3,'top',5,clusterCtl])
	mc.formLayout(form,edit=1,af=[sep_top3,'left',5])
	mc.formLayout(form,edit=1,af=[sep_top3,'right',5])

	vis = 1
	if renderer == 'vray':
		vis = 0
	mrfmCtl = mc.radioButtonGrp(nrb=2,la2=['On','Off'],l='mental ray Standalone',vis=vis,adj=1,sl=2)
	mc.formLayout(form,edit=1,ac=[mrfmCtl,'top',5,sep_top3])
	mc.formLayout(form,edit=1,af=[mrfmCtl,'left',10])
	mc.formLayout(form,edit=1,af=[mrfmCtl,'right',0])

	sep_top = mc.separator()
	mc.formLayout(form,edit=1,ac=[sep_top,'top',5,mrfmCtl])
	mc.formLayout(form,edit=1,af=[sep_top,'left',5])
	mc.formLayout(form,edit=1,af=[sep_top,'right',5])

	text2 = mc.text(l='Select chunk size for render layers:')
	mc.formLayout(form,edit=1,af=[text2,'left',0])
	mc.formLayout(form,edit=1,af=[text2,'right',0])
	mc.formLayout(form,edit=1,ac=[text2,'top',5,sep_top])

	lastCtl = str()
	for i, lay in enumerate(renderable_layers):
		intf = mc.intSliderGrp(l=lay,f=1,v=1,min=1,max=10,fmn=1,fmx=100,adj=3)
		layer_controls.append(intf)
		if i == 0:
			mc.formLayout(form,edit=1,ac=[intf,'top',5,text2])
			mc.formLayout(form,edit=1,af=[intf,'left',5])
			mc.formLayout(form,edit=1,af=[intf,'right',5])
		else:
			mc.formLayout(form,edit=1,ac=[intf,'top',0,lastCtl])
			mc.formLayout(form,edit=1,af=[intf,'left',5])
			mc.formLayout(form,edit=1,af=[intf,'right',5])
		lastCtl = intf

	submitBtn = mc.button(l='Submit',c=submit)

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
#	if (answer == "No"):
#		return 1
#	if (answer == 'Batch x 10'):
#		return 2
	return 1
	return 0
	
def check_render_mode():
	if (mc.getAttr('mentalrayGlobals.renderMode') != 0):
		answer = mc.confirmDialog(title='Check mental ray render mode', message='Render mode is not set to normal, proceed?', button=['Yes','No','Fix & Continue'], defaultButton='Fix & Continue')	
		if (answer == 'Fix & Continue'):
			mc.setAttr('mentalrayGlobals.renderMode', 0)
			maya.cmds.file(save=True)
		elif (answer == 'No'):
			mc.confirmDialog(m='Qube submission aborted!', b='Piss off.')
			return 1
	return 0

def submit(*args):
	global renderable_layers
	global layer_controls
	global window
	global rangeCtl
	global mrfmCtl
	global priorityCtl
	global cpuReserveCtl
	global timeCtl; 

	scene = mc.file(q=True, sn=True)
	if scene == '':
		mc.confirmDialog(m='Please save your scene first!', b='Damn your rules!')
		return
	
	maya.mel.eval('prepRender')
    # Set basic job properties
	job = {}
	job['prototype'] = 'cmdline'

	procs = mc.intSliderGrp(cpuReserveCtl,q=1,v=1)
	sprocs = str(procs)
	if procs == 0:
		sprocs = '1+'

	# Set the package properties
	job['package'] = {}
	job['package']['cmdline'] = 'set'

	# Sort out the priority
	pri = mc.radioButtonGrp(priorityCtl,q=1,sl=1)
	if pri == 1:
		pri = 9000
	elif pri == 2:
		pri = 5000
	elif pri == 3:
		pri = 1000
	
	job['priority'] = pri
	# temp measure
#	job['priority'] = 5000

# Create the email callback and set the address to send it to
# NOTE: Make sure that the Qube Supervisor has the email settings configured
#    job['mailaddress'] = 'yourname@your.address.com'
#    job['callbacks'] = [{'triggers':'done-job-self', 'language':'mail'}]
# Submit
#    listOfSubmittedJobs = qb.submit([job])
# Report on submit results
#    for job in listOfSubmittedJobs:
#        print job['id']
#	frames = qb.genframes(str(fs)+'-'+str(fe)+'x'+str(chunk))

	fs = mc.intFieldGrp(rangeCtl,q=1,v1=1)
	fe = mc.intFieldGrp(rangeCtl,q=1,v2=1)
	fr = int(fe) - int(fs) + 1;

	# in seconds...
	timeLimit = mc.intFieldGrp(timeCtl,q=1,v1=1) * 60;

	shot = shotName()
	maya_proj = os.path.dirname(mc.workspace(q=1,rd=1))
	maya_file = mc.file(q=1,sn=1,shn=1)
	mf = maya_file.split('.')
	maya_file_base = mf[0] 

	job['name'] = os.path.basename(scene)
	p = job['name'].split('.')
	job['name'] = p[0]

#	nuke_script = shot+'/nuke/'+job['name']+'.nk'
#	nuke_file = file(nuke_script, 'w')
#	nuke_file.write(puke_make_root(job['name'], fs, fe, format))
#	generate a nuke script
#	img = img_base+rl+'_MasterBeauty.%04d.exr'
#			nuke_file.write(puke_make_read(rl, img, fs, fe))
#	nuke_file.close()

	img_base = shot+'/images/renders/'+job['name']+'/'+job['name']

	if mc.file(q=1,amf=1):
		maya.cmds.file(save=True)

	mrsa = mc.radioButtonGrp(mrfmCtl,q=1,sl=1)

	for lc in layer_controls:
		chunk = mc.intSliderGrp(lc,q=1,v=1)
		label = mc.intSliderGrp(lc,q=1,l=1)
		joblabel = str()
		if renderer == 'vray':
			joblabel = '[vrfm]'
		elif renderer == 'mentalRay':
			if mrsa == 1:
				joblabel = '[migen]'
			else:
				joblabel = '[mrfm]'

		name = joblabel +' '+job['name']+'  :  '+label

		img = img_base+'_'+label

		if renderer == 'vray':
			ren = 'vray'
		else:
			ren = 'mr'

		grp = ''
		if renderer == 'vray':
			cmd = ['Render',
				'-r',ren,
				'-s','QB_FRAME_START',
				'-e','QB_FRAME_END',
				'-preRender','preRender',
				'-rl',label,
				'-proj',maya_proj,
				scene]
			grp = 'vray'
		elif renderer == 'mentalRay':
			if mrsa == 1:
				rendir = maya_proj+'/mentalRay/'+maya_file_base
				if not os.path.exists(rendir):
					os.makedirs(rendir)
					
				# Dump out .mi
				cmd = ['Render',
					'-binary','1',
					'-r', 'mi',
					'-perframe', '2',
					'-padframe', '4',
					'-s','QB_FRAME_START',
					'-e','QB_FRAME_END',
					'-preRender','preRender',
					'-rl',label,
					'-rd',maya_proj+'/../images/renders',
# this requires custom miRenderer.xml
#					'-passContributionMaps',
#					'-passUserData',
					'-proj',maya_proj,
					'-file',rendir+'/'+maya_file_base,
					scene]
				grp = 'migen'
			else:
				# Render using MRFM
				cmd = ['Render',
					'-lic','complete',
					'-r', 'mr',
					'-v','4',
					'-rt', str(procs),
					'-s','QB_FRAME_START',
					'-e','QB_FRAME_END',
					'-preRender','preRender',
					'-rl',label,
					'-at',
					'-aml',
					'-proj',maya_proj,
					scene]
				grp = 'mrfm'
		else:
			maya.mel.eval('warning("Unsupported renderer.")')
			return

		qmd = ['qbsub', 
			'--range', str(fs)+'-'+str(fe),
			'--chunk', str(chunk),
			'--timelimit', str(timeLimit),
			'--cpus', str(fr),
			'--padding', '4',
			'--name', name,
			'--groups', grp,
			'--priority', str(pri),
			'--reservations', 'global.maya=1,host.processors='+sprocs
			]
		qmd += cmd
		print qmd
		retval = subprocess.call(qmd)
#		maya.mel.eval('warning("Render job submitted to Qube. : '+retval+'")')
		maya.mel.eval('warning("Render job submitted to Qube.")')
#		mc.print('Render job submitted to Qube.')
	mc.deleteUI(window,wnd=1)
	
def main():
	if (renderer != 'vray'):
		if (check_render_mode()):
			return
	if (check_renderable_cameras()):
		return

	render_layers = mc.listConnections('renderLayerManager.renderLayerId')
	
	for rl in render_layers:	
		if mc.getAttr(rl+'.renderable'):
			renderable_layers.append(rl)

	confirm = confirmRender()

if __name__ == '__main__':
	main()


