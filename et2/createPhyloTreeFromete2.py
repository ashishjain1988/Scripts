#!/usr/bin/env python

import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cbook as cbook
from matplotlib.offsetbox import OffsetImage 
import matplotlib.gridspec as gridspec
import matplotlib.image as mpimg
from Bio import Phylo
from mpl_toolkits.axes_grid1 import make_axes_locatable,Size
from matplotlib.patches import Rectangle, FancyArrow
from matplotlib import cm
from PIL import Image
from os.path import expanduser
import os
import ntpath
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FixedLocator
import pickle
from matplotlib.colors import ColorConverter
from reportlab.lib import colors
from ete2 import Tree, TreeStyle, NodeStyle
import re
from Bio import SeqIO,SeqFeature
from Bio.SeqRecord import SeqRecord

finalImageHeightinMM = 2880
treeWidth = 1536

def drawete2PhylTree(treeFilePath):
    tree = Tree(treeFilePath)
    treeStyle = TreeStyle()
    treeStyle.show_scale = False
    #treeStyle.margin_left = 0
    #treeStyle.margin_right = 0
    #treeStyle.margin_top = 0
    #treeStyle.margin_bottom = 0
    #treeStyle.tree_width = treeWidth
    no_of_nodes = countNodes(tree)
    treeStyle.scale = 120#finalImageHeightinMM/no_of_nodes
    treeStyle.branch_vertical_margin = 10#finalImageHeightinMM/no_of_nodes
    #treeStyle.draw_aligned_faces_as_table = False
    tree = changeNodeStyle(tree)
    #tree.img_style["size"] = 30
    #tree.img_style["fgcolor"] = "blue"
    #tree.show(tree_style=treeStyle)
    tree.render("tree.PNG",tree_style=treeStyle,units="mm")
def countNodes(tree):
    count = 0
    for n in tree.traverse():
        count += 1
    return count

def printNodeNames(treeFilePath):
    tree = Tree(treeFilePath)
    file = open("NodeName.txt","w")
    for n in tree.traverse():
        file.write(n.name)
        file.write("\n")
        
    file.close()
    
def printAccessionNumbers(filePath):
    f = open(filePath,"r")
    o = open("accession.txt","w")
    for line in f:
        #lineSplit = line.split("_")
        o.write('_'.join(line.split('_')[2:]))
        o.write("\n")
    o.close()
    f.close()
    
def printAccessionNumbersFromName(filePath,dbFolderPath):
    file = open(filePath,"r")
    o = open("accession.txt","w")
    org = []
    accessions = []
    for line in file:
        org.append('_'.join(line.split("_")[:2]))
    for dir in return_recursive_dir_files(dbFolderPath):
        dirSplit = dir.split("/")
        organism = ""
        accession = ""
        for f in return_recursive_files(dir):
            #print f
            seq_record = SeqIO.parse(open(f), "genbank").next()
            accession = seq_record.annotations['accessions'][0]
            organism_tmp = seq_record.annotations['organism'].replace(' ', '_')
            organism_tmp_1 = re.sub('[\[\]]', "", organism_tmp)
            organism = '_'.join(organism_tmp_1.split('_')[:2])#+"_"+accession
        print organism
        try:
            if(org.index(organism) >= 0):
                accessions.append(accession)
        except:
            #print "none"
            pass
    for accesion in accessions:
        o.write(accesion+"\n")            
    o.close()
    file.close()
    
def return_recursive_dir_files(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in dir_name:
            fname = os.path.join(path, f)
            if os.path.isdir(fname):
                result.append(fname)
    return result

def return_recursive_files(root_dir):
    result = []
    for path, dir_name, flist in os.walk(root_dir):
        for f in flist:
            fname = os.path.join(path, f)
            if not os.path.isdir(fname):
                result.append(fname)
    return result

def changeNodeStyle(tree):
    # Draws nodes as small red spheres of diameter equal to 10 pixels
    nstyle = NodeStyle()
    nstyle["shape"] = "sphere"
    nstyle["size"] = 5
    nstyle["fgcolor"] = "black"

    # Gray dashed branch lines
    nstyle["hz_line_type"] = 0
    nstyle["hz_line_color"] = "black"
    for n in tree.traverse():
        n.set_style(nstyle)
    return tree

def main():
    #drawete2PhylTree("/home/jain/Downloads/ProOpDB/test_run_BSub2/tree/out_tree.nwk")
    #drawete2PhylTree("/home/jain/Downloads/NewSubtree.nwk")
    #printNodeNames("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/40_Org_tree.nwk")
    #printAccessionNumbers("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/analysis_after_strain_filtering/40_Org_tree.txt")
    printAccessionNumbersFromName("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/analysis_after_strain_filtering/40_Org_tree.txt", "/home/jain/Gram_Positive_Bacteria_Study/Proteobacteria_Genomes_Path_1/")
    #checkForSameStrain("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/analysis_after_strain_filtering/newOrgListAfterStrainFiltering.txt")

if __name__ == "__main__":
    main()