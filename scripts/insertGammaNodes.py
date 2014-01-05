# insertGammaNodes v20100520 by pink
#   insert selected gamma nodes between textures and their destinations

from pymel.core import *

def insertGammaNodes(textures):
#    print textures
    for texture in textures:
#        print texture
        destinations = connectionInfo(texture.outColor,dfs=1)
        gammaNode = shadingNode('gammaCorrect',au=1)
        gammaNode.setAttr('gammaX',.4545);
        gammaNode.setAttr('gammaY',.4545);
        gammaNode.setAttr('gammaZ',.4545);
        texture.outColor >> gammaNode.value
        for d in destinations:
#            print d
            gammaNode.outValue >> d

def main():
    # for some reason ls(textures=1,sl=1) doesn't work
    # so we build up our selected texture nodes manually
    alltex = ls(textures=1)
    seltex = ls(sl=1)
    textures = []
    for t in seltex:
        if t in alltex:
            textures.append(t)
    insertGammaNodes(textures)

if __name__ == '__main__':
    main()

# vim:ts=4:sw=4:expandtab

