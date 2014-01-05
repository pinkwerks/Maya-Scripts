from pymel.core import *

def mklist(obj):
    if isinstance(obj,list):
        return obj
    return list([obj])

def disable_all_aovs():
    # arnold aovs aren't intergrated with renderlayers the same way as mentalray
    aovs = ls(type='aiAOV')
    for aov in aovs:
        try:
            editRenderLayerAdjustment(aov+'.enabled')
        except:
            print('// Couldn\'t set render layer override for AOV '+aov+'.')
        aov.setAttr('enabled',0)
 
def ensure_cook_torrance():
    ais = ls(type='aiStandard')
    count = 0
    for ai in ais:
        v = ai.getAttr('specularBrdf')
        if v == 0 : # skip stuff set to ward_duer and cook_torrance
            ai.setAttr('specularBrdf', 2)
            count += 1
    mel.warning('Fixed '+str(count)+' nodes.')

