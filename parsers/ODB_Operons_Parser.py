#!/usr/bin/python

import time
import os
import sys
import argparse
from multiprocessing import Pool
from Bio import SeqIO
from Bio.SeqUtils import GC

# Copyright(C) 2015 Ashish Jain

def parse_file(name):
    file = open(name,'r')
    lines = file.read().splitlines()
    operons_gene_dict = {};
    for line in lines:
        lineData = line.split("\t")
        operonId = lineData[0]
        geneName = lineData[1]
        if(operons_gene_dict.has_key(operonId)):
            geneList = operons_gene_dict[operonId]
            geneList.append(geneName);
        else:
            geneList = [geneName]
        operons_gene_dict.update({operonId:geneList})
    file.close()
    return operons_gene_dict;    

def filter_operons(operons_gene_dict):
    filtered_operon_gene_list = {}
    for operon,geneList in enumerate(operons_gene_dict):
        if(len(geneList) >=5):
            filtered_operon_gene_list.update({operon:geneList})
                   
    return filtered_operon_gene_list;

def parse_regulonDB_file_and_store_results(outfolder, min_genes, url, download, experimental_only, organism_dict_for_recovery, quiet):
    #outfile = outfolder + 'gene_block_names_and_genes_unfiltered.txt'
    unfiltered_regulong_parsed_file = outfolder + 'gene_block_names_and_genes_unfiltered.txt'
    if download:
        #print "Download"
        #regulon_db(outfile, min_genes, url, download, experimental_only)
        #regulon_db(outfolder, min_genes, url, download, experimental_only, unfiltered_regulong_parsed_file)
        print "download";
    
    protein_only_list = []
    mixed_list = [] # this is a list that contains gene blocks that contain both protein coding and RNA coding genes

    gene_dict = {}
    
    # open the file that contains the pathways to each of the reference genomes (since this is regulonDB, both variants of E. coli apply
    for gene_block_line in [i.strip().split('\t') for i in open(unfiltered_regulong_parsed_file).readlines()]:
        gene_block_name = gene_block_line[0]
        gene_dict.update({gene_block_name:{}})
        #print gene_block_name
        for gene in gene_block_line[1:]:
            gene_dict[gene_block_name].update({gene:[]})
            for ref_org in sorted(organism_dict_for_recovery.keys()):
                try:
                    gene_product =  organism_dict_for_recovery[ref_org][gene][0].split('|')[7]
                    gene_dict[gene_block_name][gene].append(gene_product)
                except:
                    pass

    # there are two classes of potential products, protein and rna.  there is a list of terms that are acceptable for each
    # These two lists keep track of this, so we know what are effectively congruent terms, as we only care if they prot/rna are signaled.
    # when we determine the type of each gene block, which is RNA, protein, mixed.
    rna_list = ['tRNA', 'rRNA', 'ncRNA', ]
    protein_list = ['Protein', 'Pseudo_Gene']
    
    prot_result = []
    rna_result = []
    mixed_result = []
    
    # this can be removed later, after I later change downstream gene block file parsing
    old_result = []

    for gene_block in sorted(gene_dict.keys()):
        gene_block_error = False # If there is missing/inconsistent information in the genes then ignored the gene block
        gene_block_type = ''
        gene_list = []
        old_gene_list = []
        for gene in gene_dict[gene_block]:
            gene_type = ''
            if len(gene_dict[gene_block][gene]) == 0:
                #print gene_block, gene, "Missing annotation information"
                gene_block_error = True
            elif len(gene_dict[gene_block][gene]) == 1:
                if gene_dict[gene_block][gene][0] in protein_list:
                    gene_type = 'p'
                elif gene_dict[gene_block][gene][0] in rna_list:
                    gene_type = 'r'
                else:
                    pass
            else:
                tmp_name = gene_dict[gene_block][gene][0]
                for next_type in gene_dict[gene_block][gene][1:]:
                    if next_type in protein_list and tmp_name in protein_list:
                        gene_type = 'p'
                    elif next_type in rna_list and tmp_name in rna_list:
                        gene_type = 'r'
                    else:
                        #print gene_block, gene, "Annotation information disagrees"
                        gene_block_error = True


            gene_list.append("%s:%s" % (gene, gene_type))
            old_gene_list.append(gene)
            if gene_block_error:
                pass
            elif gene_block_type == '': # We have not evaluated the opern type (protein, RNA, mixed) yet, so set it to the type of the first gene
                gene_block_type = gene_type
            elif gene_block_type != gene_type:
                gene_block_type = 'm'
            elif gene_block_type == gene_type:
                pass
            else:
                print "The function parse_regulonDB_file_and_store_results broke from the regulon_dl_parse.py script"
        if gene_block_error:
            if not quiet:
                print "rejected gene block ", gene_block
            gene_block_error = False
        elif gene_block_type == 'p':
            prot_result.append('\t'.join([gene_block] + gene_list))
            # Remove next line after gene_block list parsing has been updated
            old_result.append('\t'.join([gene_block] + old_gene_list))
        elif gene_block_type == 'r':
            rna_result.append('\t'.join([gene_block] + gene_list))
        else:
            mixed_result.append('\t'.join([gene_block] + gene_list))
    #print "prot_result", prot_result
    #print "rna_result", rna_result
    #print "mixed_result", mixed_result
    
    
    
    
    #############################################################################################################################################
    # currently I am dumping 4 files out into the out folder. They are not selectable in terms of names, sorry. I may fix this, i may not.      #
    # the new operon format, where i have the gene names and the type of product that they code for is more useful. also we have the ability    #
    # to select prot only, rna only, or both.  To include every operon, we still would have to cat the files, which i have not done, but i      #
    # think might be a good idea.  I will look into that once we are planning on conisdering all operons. This is a simple operation. I am not  #
    # going to do it now, because after 3+ days sorting out all the bugs in this program, files, format, etc... i cannot stand the thought         #
    # of working further on this program.                                                                                                       #
    #############################################################################################################################################

    handle_prot = open(outfolder + 'gene_block_name_and_genes_prot_only.txt', 'w')
    handle_rna = open(outfolder + 'gene_block_name_and_genes_rna_only.txt', 'w')
    handle_mixed_type = open(outfolder + 'gene_block_name_and_genes_mixed_type.txt', 'w')
    
    handle_prot.write('\n'.join(prot_result))
    handle_prot.close()
    
    handle_rna.write('\n'.join(rna_result))
    handle_rna.close()
    
    handle_mixed_type.write('\n'.join(mixed_result))
    handle_mixed_type.close()
    
    handle = open(outfolder+ "gene_block_names_and_genes.txt", 'w')
    handle.write('\n'.join(old_result))
    handle.close()
    


def main():
    
    start = time.time()
    filtered_operon_list = filter_operons(parse_file(""))
    output = open("operonList.txt","w")
    for operon,geneList in enumerate(filtered_operon_list):
        s = "";
        for gene in geneList:
            s =s+"\t"+gene
        output.write(operon+"\t"+s)
    # sample input to run
    # ./regulondb_dl_parse.py -f phylo_order.txt   
if __name__ == '__main__':
    main()
