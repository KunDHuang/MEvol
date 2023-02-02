#!/usr/bin/env python

import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import multiprocessing as mp
import os
import subprocess
import argparse
import textwrap
import sys

def renaming(gene_abs_pres_df, gene_family, aln_seqs):
    # gene_abs_pres_df: the dataframe converted from gene_presence_absence.csv table generated by roary
    # gene_family: the identifier of a gene family
    # aln_seqs: the fasta file containing the aligned multiple sequences from one gene family
    
    cols_to_drop = ['Non-unique Gene name', 'Annotation', 'No. isolates',
                   'No. sequences', 'Avg sequences per isolate', 'Genome Fragment',
                   'Order within Fragment', 'Accessory Fragment',
                   'Accessory Order with Fragment', 'QC', 'Min group size nuc',
                   'Max group size nuc', 'Avg group size nuc']
    gene_abs_pres_df = gene_abs_pres_df.drop(cols_to_drop, axis = 1)
    genomes = gene_abs_pres_df.columns[1:]
    gene_family_df = gene_abs_pres_df[gene_abs_pres_df['Gene'] == gene_family]
    
    gene2genome_map = {}
    for genome in genomes:
        gene_id = gene_family_df.loc[gene_family_df['Gene'] == gene_family, genome].iloc[0]
        if not pd.isna(gene_id):
            if len(gene_id.split("\t")) > 1:
                return None
            else:
                gene2genome_map[gene_id] = genome
    
    for genome in genomes:
        gene_id = gene_family_df.loc[gene_family_df['Gene'] == gene_family, genome].iloc[0]
        if not pd.isna(gene_id):
            gene2genome_map[gene_id] = genome
    
    aln_seqs_dict = SeqIO.to_dict(SeqIO.parse(aln_seqs, 'fasta'))
    new_aln_seqs_record = [SeqRecord(seq = Seq(aln_seqs_dict[gene.id].seq.upper()),
                                                          id = gene2genome_map[gene.id],
                                                          name = gene2genome_map[gene.id],
                                                          description = gene2genome_map[gene.id]) for gene in SeqIO.parse(aln_seqs, 'fasta')]
    
    return new_aln_seqs_record

def create_folder(name):
    folder_name = os.path.abspath(name) # determine the abs path
    if os.path.exists(folder_name):
        pass
    else:
        os.makedirs(folder_name)
    return folder_name

def renamingNoutput(args):
    
    gene_abs_pres_df, gene_family, aln_seqs, opt_dir = args
    
    aln_seqs_record4opt = renaming(gene_abs_pres_df, gene_family, aln_seqs)
    if aln_seqs_record4opt:
        opt_aln_file = create_folder(opt_dir) + '/' + gene_family + '.fa.aln'
        SeqIO.write(aln_seqs_record4opt, opt_aln_file, "fasta")
        return opt_aln_file
    else:
        return None

def renamingNoutput_nproc(gene_abs_pres_df, aln_seqs_files, opt_dir_path, nproc = 2):
    # gene_abs_pres_df: the dataframe converted from gene_presence_absence.csv table generated by roary
    # gene_families: a list of gene family identifiers
    # aln_seqs_files: a list of sequence alignment files
    # opt_dir_path: the output directory for storing renamed files
    opt_dir_path = create_folder(opt_dir_path)
    packed_args = [(gene_abs_pres_df, os.path.basename(aln_seqs_file).split(".")[0], aln_seqs_file, opt_dir_path) for aln_seqs_file in aln_seqs_files]
    pool = mp.Pool(processes = nproc)
    opt_files = pool.map(renamingNoutput, packed_args)
    return opt_files
    
def clean_df(df):
    # replace special characters with '_' in the Gene column
    # so that gene names in the gene absence and presence table can be matched with multiple sequence alignment files.
    special_chars = list(r"""`~!@#$%^&*()_-+={[}}|\:;"'<,>.?/""")
    for i in special_chars:
        df['Gene'] = df['Gene'].str.replace(i, '_', regex=True)
        
    return df    

def screen_aln_files(gene_abs_pres_df, aln_files):
    genes = gene_abs_pres_df['Gene'].to_list()
    screened_aln_files = []
    problematic_aln_files = []
    for aln_file in aln_files:
        gene_family_name = os.path.basename(aln_file).split(".")[0]
        if gene_family_name in genes:
            screened_aln_files.append(aln_file)
        else:
            problematic_aln_files.append(aln_file)
    
    return screened_aln_files, problematic_aln_files
    
if __name__ == "__main__":
    def read_args(args):
    # This function is to parse arguments

        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description = textwrap.dedent('''\
                                         This program is to replace gene names in each multiple sequence alignment file with their corresponding genome names.
                                         '''),
                                        epilog = textwrap.dedent('''\
                                        examples: original_name_finder.py --gene_table gene_presence_absence.csv --gene_family_dir pan_genome_sequences --nproc 10 --opt_dir test_opt
                                       '''))
        parser.add_argument('--gene_table',
                        nargs = '?',
                        help = 'Input the gene absence and presence table from Roary (i.e. gene_presence_absence.tsv).',
                        type = str,
                        default = None)

        parser.add_argument('--gene_family_dir',
                        nargs = '?',
                        help = 'Specify the the directory containing multiple sequence alignments of gene families. Note: file pattern should be same as Roary outputs',
                        type = str,
                        default = None)
                        
        parser.add_argument('--nproc',
                        nargs = '?',
                        help = 'Specify the number of CPUs you want to use. zero-based and default: [2]',
                        type = int,
                        default = 1)    

        parser.add_argument('--opt_dir',
                        nargs = '?',
                        help = 'Specify the output folder name where individual files will be stored. default: [output_dir]',
                        type = str,
                        default = 'output_dir')    

        return vars(parser.parse_args())
    
        
    pars = read_args(sys.argv)
    gene_abs_pres_df = pd.read_csv(pars['gene_table'], index_col = False, low_memory = False)
    gene_abs_pres_df = clean_df(gene_abs_pres_df)    
    alns = subprocess.getoutput("ls {}/*".format(pars['gene_family_dir'])).split("\n")
    qc_files = screen_aln_files(gene_abs_pres_df, alns)
    postqc_alns = qc_files[0]
    problem_alns = qc_files[1]
    if len(problem_alns) > 0:
        warning_info = ["Gene alignment files belowe could not be found in the gene presence and absence table, please check the naming consistency:"] + problem_alns
        warning_info = "\n".join(warning_info) + "\n"
        sys.stdout.write(warning_info)    
    renamingNoutput_nproc(gene_abs_pres_df, postqc_alns, pars['opt_dir'], pars['nproc'])
    
    











