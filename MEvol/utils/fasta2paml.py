#!/usr/bin/env python

from Bio import SeqIO
import sys
import re
import subprocess
import argparse
import textwrap
import os

"""
NAME: fasta2paml.py
DESCRIPTION: fasta2paml.py is a script/module to convert fasta format to paml format
AUTHOR: Kun D. Huang
DATE: 01.02.2023
"""

def paml_structure(fasta):
    # fasta: the fasta file
    # This function is to convert a multiple sequence alignment in fasta format to paml format. It returns string
    def seq_breaker(seq):
        # seq: a seq in str
        if len(seq) <= 60:
            return seq
        else:
            seq = re.sub("(.{60})", "\\1\n", seq, 0, re.DOTALL)
            if seq.endswith("\n"):
                seq = seq
            else:
                seq = seq + "\n"
            return seq
            
    seq_records = list(SeqIO.parse(fasta, "fasta"))
    nr_seqs = str(len(seq_records))
    seq_lens = [len(i.seq) for i in seq_records]
    
    if len(set(seq_lens)) == 1:
        nr_nuc = str(seq_lens[0])
    else:
        sys.exit("Sequences have different length. Please make sure they are aligned. Error: {}".format(fasta))
    
    paml_list = ["   {}   {}\n".format(nr_seqs, nr_nuc)]
    for seq_rec in seq_records:
        paml_list.append(seq_rec.id + "\n")
        
        paml_list.append(seq_breaker(str(seq_rec.seq.upper())))
        
        
    paml_str = "".join(paml_list)
    
    return paml_str

def multi_paml_structure(fasta_list):
    # fasta_list: a list of fasta files
    # This function is to convert multiple fasta-formated multuple sequence alignments to paml format, in one paml file.
    paml_str_list = [paml_structure(fasta) for fasta in fasta_list]
    
    return "".join(paml_str_list)

if __name__ == "__main__":
    def read_args(args):
    # This function is to parse arguments

        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description = textwrap.dedent('''\
                                         This program is to convert FASTA file/files to a PAML file.
                                         '''),
                                        epilog = textwrap.dedent('''\
                                        examples: snv_estimator.py --fasta yvcJ.fa.aln --opt_tab yvcJ_snvrates.tsv
                                       '''))
        parser.add_argument('--fasta_in',
                        nargs = '?',
                        help = 'Input a FASTA file which contains aligned multiple sequences.\
                            If you want you merge multiple fasta files in one paml file you can input a folder of FASTA files.',
                        type = str,
                        default = None)

        parser.add_argument('--paml_out',
                        nargs = '?',
                        help = 'Specify the name for the PAML output file.',
                        type = str,
                        default = None)
        return vars(parser.parse_args())    
    
    pars = read_args(sys.argv)
    fasta_in = os.path.abspath(pars['fasta_in'])
    if os.path.isdir(fasta_in):
        fasta_files = subprocess.getoutput("ls {}/*".format(fasta_in)).split("\n")
        paml_out = multi_paml_structure(fasta_files) 
    elif os.path.isfile(fasta_in):
        paml_out = paml_structure(fasta_in)
        
    opt_paml = open(os.path.abspath(pars['paml_out']), "w")
    opt_paml.write(paml_out)
    opt_paml.close()    
        
        
    
