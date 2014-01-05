#!/bin/env python
# vim:ts=4:sw=4:expandtab
# ensure unique names in maya
# crafted with love, by pink
# not the fastest algorithm, but it works

import maya.cmds as mc

def byDepth(word1, word2):
    a = word1.split('|')
    b = word2.split('|')
    return len(a) - len(b)

def main():
    id = 0
    while 1:
        everything = mc.ls()
    # this slows things down... but it prints nicer
        everything.sort(cmp=byDepth)
        longnames = list()

        for thing in everything:
            if len(thing.split('|')) > 1:
                longnames.append(thing)

        if len(longnames) == 0:
            print '# Renamed '+str(id)+' nodes'
            break

        o = longnames.pop()
        name = o.split('|').pop()
        mc.select(o)
        print '# '+o+' -> '+name+str(id)
        mc.rename(name+str(id))
        id += 1

if __name__ == '__main__':
    main()

