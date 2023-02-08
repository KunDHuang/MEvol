#!/usr/bin/env python

import os
import sys
import subprocess
import argparse
import textwrap

"""
NAME: codeml_fline.py (Forward Line)
DESCRIPTION: codeml_fline.py is acting as the forward line of codeml script family to prepare all required data prior to running codeml
AUTHOR: Kun D. Huang
DATE: 08.02.2023
"""

def create_folder(name):
    folder_name = os.path.abspath(name) # determine the abs path
    if os.path.exists(folder_name):
        pass
    else:
        os.makedirs(folder_name)
    return folder_name


def append_mevol_ctl(paml_file, paml_tree, outdir, appendix = None):
    # mevol_ctl: the base Mevol-codeml control file.
    # paml_file: the paml file containing multuple sequence alignment.
    # paml_tree: the tree structure in the format of PAML tree
    # outdir: the directory holding output files.
    # appendix: if you want to append some identifiers to output, e.g. M012 , using Model 0, 1, 2
    
   # codeml version 4.9, March 2015
    mevol_ctl = [('runmode', '0'),
                 ('seqtype', '1'),
                 ('CodonFreq', '2'),
                 ('ndata', '1'),
                 ('clock', '0'),
                 ('model', '0'),
                 ('NSsites', '0 1 2'),
                 ('icode', '0'),
                 ('fix_omega', '0'),
                 ('omega', '.4'),
                 ('cleandata', '1')]

    outdir = create_folder(outdir)
    paml_file = os.path.abspath(paml_file)
    paml_tree = os.path.abspath(paml_tree)
    if appendix:
        codeml_opt = outdir + "/" + os.path.basename(paml_file).split(".")[0] + "_{}".format(appendix) +".mlc"
    else:
        codeml_opt = outdir + "/" + os.path.basename(paml_file).split(".")[0] + ".mlc"
    
    mevol_ctl.insert(0, ('outfile', codeml_opt))
    mevol_ctl.insert(0, ('treefile', paml_tree))
    mevol_ctl.insert(0, ('seqfile', paml_file))
    
    ctl_opt = codeml_opt.replace("mlc", "ctl")
    return mevol_ctl, ctl_opt




if __name__ == "__main__":
    def read_args(args):
    # This function is to parse arguments

        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description = textwrap.dedent('''\
                                         This program is a frontline script to prepare all materials for running codeml.
                                         '''),
                                        epilog = textwrap.dedent('''\
                                        examples: 
                                       '''))
        parser.add_argument('--paml_file',
                        nargs = '?',
                        help = 'Specify the location to the PAML file containing multiple sequence alignment.',
                        type = str,
                        default = None)

        parser.add_argument('--paml_tree',
                        nargs = '?',
                        help = 'Specify the location to the PAML tree.',
                        type = str,
                        default = None)
        parser.add_argument('--opt_dir',
                        nargs = '?',
                        help = 'Specify the output directory.',
                        type = str,
                        default = None)
        parser.add_argument('--id_appendix',
                        nargs = '?',
                        help = 'Specify an identifier to append to outputs. Default: None',
                        type = str,
                        default = None)        
        return vars(parser.parse_args())
    
    pars = read_args(sys.argv)
        
    mevol_ctl, ctl_opt = append_mevol_ctl(pars['paml_file'], pars['paml_tree'], pars['opt_dir'], pars['id_appendix'])
    opt_ctl_file = open(ctl_opt, 'w')
    for i in mevol_ctl:
        opt_ctl_file.write("{} = {}\n".format(i[0], i[1]))