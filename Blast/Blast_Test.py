#!/usr/bin/python

from multiprocessing import Pool
import time
import os
import sys
import argparse
from Bio.Blast.Applications import NcbiblastxCommandline
from Bio import Phylo

def writeToFile(name):
    target = open(name,'w')
    target.write("This is my first write file");
    target.close();
def createNewickTreeDrawAscii(name,name1):
    tree=Phylo.read(name,"newick")
    target = open(name1,'w+');
    Phylo.draw_ascii(tree,target)
    target.close();
def createNewickTreeDrawGraphviz(name,name1):
    tree=Phylo.read(name,"newick")
    target = open(name1,'w+');
    Phylo.draw_ascii(tree,target)
    target.close();
    

name = "out_tree.nwk"
name1 = "phylo.png";
print "This is run"
#writeToFile(name);
createNewickTreeDrawAscii(name,name1);
    