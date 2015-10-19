#!/usr/bin/env python

import numpy as np
import os
from Bio import SeqIO,SeqFeature
from Bio.SeqRecord import SeqRecord
from Bio import Application
from Bio.Application import _Option
from Bio.Align.Applications import ClustalwCommandline
from Bio import Phylo
import re

def filterStrain(handle,outHandle):
    distinctSpeciesDict = {}
    for i in handle:
        lineData = i.split("\t")
        strainName = lineData[0].strip();
        folderPath = lineData[1].strip();
        #print folderPath
        #print str(return_recursive_files(folderPath)) + "\n"
        print strainName
        for f in return_recursive_files(folderPath):
            seq_record = SeqIO.parse(open(f), "genbank").next()
            accession = seq_record.annotations['accessions'][0]
            organism_tmp = seq_record.annotations['organism'].replace(' ', '_')
            organism_tmp_1 = re.sub('[\[\]]', "", organism_tmp)
            organism = '_'.join(organism_tmp_1.split('_')[:2])#+"_"+accession
            #print organism
            if accession == 'NC_022759':
                print "found"
            if(distinctSpeciesDict.has_key(organism)):
                oldFilePath = distinctSpeciesDict[organism]
                old_record = SeqIO.parse(open(oldFilePath), "genbank").next()
                old_accession = old_record.annotations['accessions'][0]
                if(old_accession > accession):
                    distinctSpeciesDict.update({organism:f})
            else:
                distinctSpeciesDict.update({organism:f})
                if accession == 'NC_022759':
                    print "not found" 
    #print len(distinctSpeciesDict)
    for key,value in distinctSpeciesDict.iteritems():
        outHandle.write(key+"\t"+os.path.dirname(value)+"\n")            
    
        
def return_recursive_files(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in flist:
            fname = os.path.join(path, f)
            if not os.path.isdir(fname):
                result.append(fname)
    return result

def return_recursive_dir_files(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in dir_name:
            fname = os.path.join(path, f)
            if os.path.isdir(fname):
                result.append(fname)
    return result

def deletePlasmids(rootDir):
    #for path, dir_name, flist in os.walk(rootDir):
        #fileOut = open("morethan1chr.txt","w") 
        for file in return_recursive_dir_files(rootDir):
            #print file
            #if os.path.isdir(file):
                #print file
                files = return_recursive_files(file)
                #print str(file) + str(files)
                fileName = ""
                if len(files) > 1:
                    for f in files:
                        #print f
                        seq_record = SeqIO.parse(open(f), "genbank").next()
                        accession = seq_record.annotations['accessions'][0]
                        organism_tmp = seq_record.annotations['organism'].replace(' ', '_')
                        organism_tmp_1 = re.sub('[\[\]]', "", organism_tmp)
                        organism = '_'.join(organism_tmp_1.split('_')[:2])#+"_"+accession
                        definition = seq_record.description;
                        #print def
                        if ("plasmid" not in definition):
                            if fileName != "":
                                print "error"
                                print file.split("/")[4]
                                #fileOut.write(file.split("/")[4]+"\n")
                            fileName = accession+".gbk"
                            #print fileName 
                    for f in files:
                        #print os.path.basename(f)
                        if os.path.basename(f) != fileName:
                            os.remove(f)
                            #print "remove file "+f
        #fileOut.close()                    
                            
def main():
    handle = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/newOrgListAfterStrainFiltering.txt","r")
    #outHandle = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/filter_strain.txt","w")
    #filterStrain(handle,outHandle)
    #outHandle.close()
    handle.close()
    deletePlasmids("/home/jain/Gram_Positive_Bacteria_Study/Proteobacteria_Genomes_Path_1")
    

if __name__ == "__main__":
    main()