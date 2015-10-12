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

def checkForSameStrain(filePath):
    f = open(filePath,"r")
    o = open("accession.txt","w")
    list = []
    for line in f:
        #lineSplit = line.split("_")
        org = '_'.join(line.split('_')[:2])
        #print org
        try:
            if(list.index(org) >= 0):
                print org
        except:
            list.append(org)
            #print org
    o.close()
    f.close()

def main():
    #drawete2PhylTree("/home/jain/Downloads/ProOpDB/test_run_BSub2/tree/out_tree.nwk")
    #drawete2PhylTree("/home/jain/Downloads/NewSubtree.nwk")
    #printNodeNames("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/40_Org_tree.nwk")
    #printAccessionNumbers("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/40_Org_tree.txt")
    checkForSameStrain("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Proteobacteria/40_Org_tree.txt")

if __name__ == "__main__":
    main()