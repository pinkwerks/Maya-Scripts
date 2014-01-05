import maya.cmds as mc

def main():
	myObjects = mc.ls(selection=True)
	if len(myObjects) >= 1:
		myXforms = mc.xform(myObjects[0], q=True, m=True, ws=True)
		mc.xform(myObjects[1:], ws=True, m=myXforms)
	else:
		maya.mel.eval('warning("Nothing selected")')

if __name__ == "__main__":
    main()
