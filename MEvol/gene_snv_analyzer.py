#!/usr/bin/env python

"""
NAME: snv_analyzer.py
DESCRIPTION: gene_snv_analyzer.py is a python script for analyzing pairwise SNV rates of single multiple sequence alignments
             collectively representing the pangenome of a species.
Author: Kun D. Huang
Date: 30.01.2023
"""

"""
Main features:
1. It takes as input a folder of pangenome multiple sequence alignments.
2. It first selects a collection of gene alignments for further analysis, the coreness threshold for chosing a gene
   can be given by a user or automatically being decided using the maximum number of sequences in the gene alignments.
3. It can optionally start from raw outputs from roary by providing needed input files.
4. It multiprocess gene alignments using the number of CPUs given by a user.
5. The fixed output is a folder of files containing pairwise SNV rates.
6. Optionally output can be a file containing the averaged SNV rates for each gene.  
"""

def select_gene_alns(gene_alns_list, coreness = None):
    # gene_alns_list: a list of gene alignment fasta files.
    # coreness: the minimum genenome a gene alignment fasta file should contain for deteriming a gene as a core gene of one species.
    

