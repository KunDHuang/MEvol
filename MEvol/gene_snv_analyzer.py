#!/usr/bin/env python

import subprocess
import multiprocessing as mp
from Bio import SeqIO
import pandas as pd
import os
import subprocess
import argparse
import textwrap
import sys
import tempfile
from utils.original_name_finder import renamingNoutput_nproc, clean_df, screen_aln_files, select_gene_alns

"""
NAME: snv_analyzer.py
DESCRIPTION: gene_snv_analyzer.py is a python script for analyzing pairwise SNV rates of single multiple sequence alignments
             collectively representing the pangenome of a species.
Author: Kun D. Huang
Date: 30.01.2023
"""

def read_args(args):
   # This function is to parse arguments

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description = textwrap.dedent('''\
                                     This program is to replace gene names in each multiple sequence alignment file with their corresponding genome names.
                                         '''),
                                     epilog = textwrap.dedent('''\
                                        examples:gene_snv_analyzer.py --gene_family_dir pan_genome_sequences --gene_table gene_presence_absence.csv --nproc 10 --opt_dir output_dir --concat_tab concat_snv_rates.tsv 
                                       '''))

    parser.add_argument('--gene_family_dir',
                        nargs = '?',
                        help = 'Specify the the directory containing multiple sequence alignments of gene families. Note: file pattern should be same as Roary outputs',
                        type = str,
                        default = None)
    
    parser.add_argument('--metadata',
                        nargs = '?',
                        help = 'Input the metadata you would like to append to the pairwise SNV rates. Note: metadata in character will be combined using $, e.g. Vegan$Omnivore. \
                            metadata in numeric will be presented by difference (seq1 - seq2), e.g. 1.5',
                        type = str,
                        default = None)
                        
    parser.add_argument('--entry_col',
                        nargs = '?',
                        help = 'Specify the column which contains the entries (i.e. FASTA headers). Use this feature only when --metadata option is being used. \
                            The first column will be used as default if this option is not specified.',
                        type = str,
                        default = None)
        
    parser.add_argument('--cols_kept_o_rm',
                        nargs = '?',
                        help = "Input the metadata columns you want to keep (e.g. k,Diet,BMI) or remove (e.g. r,Diet,BMI) from the whole input metadata table. default [None].\
                                Use this feature only when --metadata option is being used.",
                        type = str,
                        default = None)
                           
    parser.add_argument('--nproc',
                        nargs = '?',
                        help = 'Specify the number of CPUs you want to use. zero-based and default: [2]',
                        type = int,
                        default = 1)    

    parser.add_argument('--coreness',
                        nargs = '?',
                        help = 'Specify the minimum number of genomes across a gene for this gene to be determined as core gene. Default, the maximum number of genomes (automated estimation) in the all core genes. Note: 1 is the minimum input number',
                        type = float,
                        default = None)
    
    parser.add_argument('--gene_table',
                        nargs = '?',
                        help = 'Input the gene absence and presence table from Roary (i.e. gene_presence_absence.tsv), if your multiple sequences are labeled by gene names instead of genome names.',
                        type = str,
                        default = None)

    parser.add_argument('--opt_dir',
                        nargs = '?',
                        help = 'Specify the output folder name where individual files will be stored. default: [output_dir]',
                        type = str,
                        default = 'output_dir')
    
    parser.add_argument('--concat_tab',
                        nargs = "?",
                        help = 'Specify the name of an output file if you want to concatenate individual gene alignments in one table. default: [None]',
                        type = str,
                        default = None)    

    return vars(parser.parse_args())

def call_snv_estimator(args):
    gene_aln, metadata, entry_id, cols_keep_o_rm, opt_tab = args
    snv_estimator = os.path.dirname(os.path.abspath(__file__)) + "/utils/snv_estimator.py"
    conv = lambda i : i or '' # convert None to empty string 
    cmd = "{} --fasta {} --metadata {} --entry_col {} --cols_kept_o_rm {} --opt_tab {}".format(snv_estimator,
                                                                                               gene_aln,
                                                                                               conv(metadata),
                                                                                               conv(entry_id),
                                                                                               conv(cols_keep_o_rm),
                                                                                               opt_tab)
    subprocess.call(cmd, shell = True)
    return opt_tab
 
def calc_gene_snv_nproc(gene_alns, opt_dir, cols_keep_o_rm = None, entry_id = None, metadata = None, nproc = 1):
    # gene_alns: A list of gene alignment files for calculating pariwise SNV rates.
    # metadata: the metadata dataframe for appending to estimated SNV rates.
    # nproc: the number of processors you would like to use, default [1]
    opt_dir = create_folder(opt_dir) + "/snv_rate_files"
    opt_dir = create_folder(opt_dir)


    pool = mp.Pool(processes = nproc)
    packed_args = []
    for gene_aln in gene_alns:
       opt_tab = opt_dir + "/" + os.path.basename(gene_aln).split(".")[0] + "_snvrates.tsv"
       packed_args.append([gene_aln, metadata, entry_id, cols_keep_o_rm, opt_tab])
    snv_rate_files = pool.map(call_snv_estimator, packed_args)
    
    return snv_rate_files

def create_folder(name):
    folder_name = os.path.abspath(name) # determine the abs path
    if os.path.exists(folder_name):
        pass
    else:
        os.makedirs(folder_name)
    return folder_name        
   
if __name__ == "__main__":
    pars = read_args(sys.argv)
    gene_alns = subprocess.getoutput("ls {}/*".format(pars['gene_family_dir'])).split("\n")
    if pars['gene_table']:
        tmp_folder = tempfile.mkdtemp(dir = create_folder(pars['opt_dir'])) # make a temporary file in the current directory
        gene_abs_pres_df = pd.read_csv(pars['gene_table'], index_col = False)
        gene_abs_pres_df = clean_df(gene_abs_pres_df)
        qc_files = screen_aln_files(gene_abs_pres_df, gene_alns)
        gene_alns = qc_files[0]
        problem_alns = qc_files[1]
        if len(problem_alns) > 0:
            warning_info = ["Gene alignment files belowe could not be found in the gene presence and absence table, please check the naming consistency:"] + problem_alns
            warning_info = "\n".join(warning_info) + "\n"
            sys.stdout.write(warning_info)                                     
        gene_alns = renamingNoutput_nproc(gene_abs_pres_df,
                                         gene_alns,
                                         tmp_folder,
                                         pars['nproc']
                                         )
    gene_alns = [gene_aln for gene_aln in gene_alns if gene_aln is not None]
    gene_alns = select_gene_alns(gene_alns, coreness = pars['coreness'])
   
    gene_snv_files = calc_gene_snv_nproc(gene_alns, pars['opt_dir'], cols_keep_o_rm = pars['cols_kept_o_rm'], entry_id = pars['entry_col'], metadata = pars['metadata'], nproc = pars['nproc'])
   
    if pars['concat_tab']:
        opt_concat_tab = pars['opt_dir'] + '/' + pars['concat_tab']
        concat_df = pd.concat([pd.read_csv(gene_snv_file, sep = '\t', index_col = False) for gene_snv_file in gene_snv_files])
        concat_df.to_csv(opt_concat_tab, sep = '\t', index = False)
