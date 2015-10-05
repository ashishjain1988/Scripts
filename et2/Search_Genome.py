#!/usr/bin/env python

import os
import sys
import time
import argparse
import shutil
from Bio import SeqIO,SeqFeature
from Bio.SeqRecord import SeqRecord
from Bio import Application
from Bio.Application import _Option
from Bio.Align.Applications import ClustalwCommandline
from Bio import Phylo
import subprocess

def return_recursive_dir_files(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in flist:
            fname = os.path.join(path, f)
            if os.path.isdir(fname):
                result.append(fname)
    return result

def return_file_list(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in flist:
            fname = os.path.join(path, f)
            if os.path.isfile(fname):
                result.append(fname)
    return result

def make_common_to_accession_dict(infolder):
    org_paths = return_file_list(infolder)
    common_to_accession_dict = {}
    for org in org_paths:
        seq_record = SeqIO.parse(open(org), "genbank").next()
        accession = seq_record.annotations['accessions'][0]
        organism_tmp = seq_record.annotations['organism'].replace(' ', '_')
        organism = '_'.join(organism_tmp.split('_')[:2])
        common_to_accession_dict.update({organism:accession})
    file = open("filter_file.txt","w")
    for key,value in common_to_accession_dict.iteritems():
        file.write(value+"\n");
    file.close()
    
def creating_filter_list(infolder):
    files = return_file_list(infolder)
    filterFile = open("filter.txt","w")
    for file in files:
        filterFile.write(file.split("/")[6].split(".")[0])
        filterFile.write("\n")
    filterFile.close()

def main():
    genomesPath = "/home/jain/Gram_Positive_Bacteria_Study/Gram_Positive_Bacteria_Genomes"
    filteredGenomes = "/home/jain/workspace/Scipts/et2/NodeName.txt"
    list_of_genomes = return_recursive_dir_files(genomesPath)
    fullGenomesList = []
    #make_common_to_accession_dict(genomesPath)
    for line in open(filteredGenomes):
        #print line
        for i in list_of_genomes:
            if(i.find(line)):
                fullGenomesList.append(i)
                break
            
    for i in fullGenomesList:
        print i
    creating_filter_list("/home/jain/Gram_Positive_Bacteria_Study/Bacillus_Genomes_Path/")
        
if __name__ == "__main__":
    main()
    
        