#!/usr/bin/env python

from subprocess import Popen, PIPE
import sys
import subprocess
import argparse
import textwrap
import os
import time
"""
NAME: codeml_puppeteer.py
DESCRIPTION: codeml_pupeteer.py is a puppeteer script to run codeml which is the puppet 
AUTHOR: Kun D. Huang
DATE: 07.02.2023
"""

def puppeteer_func(puppet_software, puppet_input):
    puppet_cmd = "{} {}".format(puppet_software, puppet_input)
    proc = Popen([puppet_cmd], stdin = PIPE, shell = True)
    proc.communicate(input = b'\n')
    
    return

def create_folder(name):
    folder_name = os.path.abspath(name) # determine the abs path
    if os.path.exists(folder_name):
        pass
    else:
        os.makedirs(folder_name)
    return folder_name

if __name__ == "__main__":
    
    def read_args(args):
    # This function is to parse arguments

        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description = textwrap.dedent('''\
                                         This program is to run codeml from python interface.
                                         '''),
                                         epilog = textwrap.dedent('''\
                                         examples: snv_estimator.py --pupet_clt codeml-M0.ctl
                                         '''))
        parser.add_argument('--puppet_tool',
                        nargs = '?',
                        help = 'Input the absolute path to the puppet tool. Default: [/vol/projects/khuang/tools/paml/bin/codeml]',
                        type = str,
                        default = '/vol/projects/khuang/tools/paml/bin/codeml')

        parser.add_argument('--puppet_clt',
                        nargs = '?',
                        help = 'Input the codeml control file which instructs codeml analysis.',
                        type = str,
                        default = None)
        
        parser.add_argument('--working_dir',
                        nargs = '?',
                        help = 'Specify the directory under which you want puppet to work.',
                        type = str,
                        default = None)
        return vars(parser.parse_args())    
    
    pars = read_args(sys.argv)
    if pars['working_dir']:
        wd = create_folder(pars['working_dir'])
        os.chdir(wd)
    puppeteer_func(pars['puppet_tool'], pars['puppet_clt'])
    
