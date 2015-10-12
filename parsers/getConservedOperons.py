#!/usr/bin/env python

import numpy as np
from Bio import Phylo
from PIL import Image
from os.path import expanduser
import os
import ntpath
import pickle
from gc import disable


PATH = "/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Bacteroidetes/Run_filter_E-Value_1e-10/"
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
    operonTotalConsDict = {}
    operonEventConsDict = {}    
    for operon in operonDistanceDict:
        distance = 0
        no_of_orgs = operonKeysDict[operon]
        operonDistDict = operonDistanceDict[operon]
        for event,value in operonDistDict.iteritems():
            distance +=value
        normFactor = (no_of_orgs*(no_of_orgs-1))/2.0
        if(no_of_orgs != 1):
            operonTotalConsDict.update({operon:(distance/normFactor)})
            operonEventConsDict.update({operon:{'deletions':(operonDistDict['deletions']/normFactor),'splits':(operonDistDict['splits']/normFactor),'duplications':(operonDistDict['duplications']/normFactor)}})
        else:
            operonTotalConsDict.update({operon:0})
            operonEventConsDict.update({operon:{'deletions':0,'splits':0,'duplications':0}}) 
        
    handle = open(PATH+"conservedOperonsSorted.txt","w")
    handle.write("Operon Name\tTotal C.Score\tDeletion C.Score\tSplits C.Score\tDuplications C.Score\n")
    for operon in sorted(operonTotalConsDict.items(), key=lambda x: x[1]):
        if(operonKeysDict[operon[0]] >=30):
            operonName = operon[0]
            handle.write("%s\t%.4f\t%.4f\t%.4f\t%.4f" % (operonName,operon[1],operonEventConsDict[operonName]['deletions'],operonEventConsDict[operonName]['splits'],operonEventConsDict[operonName]['duplications']))
            handle.write("\n")
    handle.close()

def main():
    #print "Main"
    event_dist = pickle.load(open(PATH+"gene_block_distance_matrices/event_dict.p"))
    getConservedOperonsList(event_dist)

if __name__ == "__main__":
    main()