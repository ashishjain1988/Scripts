#!/usr/bin/env python

import os
import sys

def filter(handle,trueFile,falseFile):
    for line in handle:
        flag = line.split(" ")[0]
        accession = line.split(" ")[1]
        if(flag == "True"):
            trueFile.write(accession+"\n")
        else:
            falseFile.write(accession+"\n")

def main():
    handle = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Firmicutes/Firmicutes_Genome_Flag.txt",'r');
    trueFile = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Firmicutes/firmicutes_with_marker.txt","w")
    falseFile = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Firmicutes/firmicutes_without_marker.txt","w")
    filter(handle, trueFile, falseFile)
    trueFile.close()
    falseFile.close()
    handle.close() 
        
if __name__ == "__main__":
    main()