# reverse the order of the selection
# --pink
import maya.cmds as mc

sel = mc.ls(sl=True)
sel.reverse()
mc.select(sel)

