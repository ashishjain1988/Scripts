#!/usr/bin/env python

import numpy as np
from Bio import Phylo
from PIL import Image
from os.path import expanduser
import os
import ntpath
import pickle
from gc import disable

def getConservedOperonsList(pickleObj):
    #print pickleObj.keys()[0]
    #print pickleObj[pickleObj.keys()[1]]
    operonDistanceDict = {}
    operonKeysDict = {}
    for operon in pickleObj.keys():#operon
        orgDistanceDict = pickleObj[operon]
        deletion = 0
        duplications = 0
        splits = 0
        operonKeysDict.update({operon:len(pickleObj[operon].keys())})
        for orgs in orgDistanceDict.keys():#one org
            specieDistance = orgDistanceDict[orgs]
            for org in specieDistance.keys():
                distanceDict = specieDistance[org]
                deletion += distanceDict['deletions']
                splits += distanceDict['splits']
                duplications += distanceDict['duplications']
                #print "In organism %s the deletions are %d, the splits %d and the duplications are %d \n",org,deletion,splits,duplications
        operonDistanceDict.update({operon:{'deletions':deletion,'splits':splits,'duplications':duplications}})
    operonTotalDistDict = {}    
    for operon in operonDistanceDict:
        distance = 0
        no_of_orgs = operonKeysDict[operon]
        for event,value in operonDistanceDict[operon].iteritems():
            distance +=value
        operonTotalDistDict.update({operon:(distance*1.0/no_of_orgs)})
    handle = open("conservedOperonsSorted.txt","w")
    for operon in sorted(operonTotalDistDict.items(), key=lambda x: x[1]):
        #print operon
        if(operonKeysDict[operon[0]] >=5):
            handle.write(str(operon))
            handle.write("\n")
    handle.close()

def main():
    #print "Main"
    event_dist = pickle.load(open("/home/jain/Gram_Positive_Bacteria_Study/Test_Run_Test/gene_block_distance_matrices/event_dict.p"))
    getConservedOperonsList(event_dist)

if __name__ == "__main__":
    main()