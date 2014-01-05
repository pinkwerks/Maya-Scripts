print "PINKWERKS : Using ~/maya/scripts/userSetup.py"
import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as OpenMaya

#if mel.getApplicationVersionAsFloat() >= 2011:
#   from pymel.core import *

try:
   import renderUtils
except:
   pass

#import sys
#sys.path.append("c:/Users/cbonnstetter/Documents/maya/scripts")

def pyError( errorString ):
   """ print an error message """
   try: 
      mel.eval(_NOL10N('error "%s"') % errorString)
   except: 
      pass

def pyWarning( warningString ):
   """ print a warning message """
   try: 
      mel.eval(_NOL10N('warning "%s"') % warningString)
   except: 
      pass

#if cmds.commandPort(':7720', q=True) !=1:
#    cmds.commandPort(n=':7720', eo = False, nr = True)

#def initMaya():
#    kToolsRoot = "TOOLS_ROOT"
#    toolsRoot = "/tools/release"
#    if kToolsRoot in os.environ:
#        if os.path.exists( os.environ[kToolsRoot] ):
#            toolsRoot = os.environ[kToolsRoot]
#        else:
#            print( "WARN : %s does not exist, using defaults" % os.environ[kToolsRoot] )
#    print( "INFO : TOOLS_ROOT=%s" % toolsRoot )
#   
#    sys.path.append( os.path.join( toolsRoot, "maya/scripts/py" ) )
#    pass
#
#initMaya()
