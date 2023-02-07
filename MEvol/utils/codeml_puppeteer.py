#!/usr/bin/env python

from subprocess import Popen, PIPE
import sys
import subprocess
import argparse
import textwrap

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
                        help = 'Input the absolute path to the puppet tool. Default: [/vol/projects/khuang/anaconda3/bin/codeml]',
                        type = str,
                        default = '/vol/projects/khuang/anaconda3/bin/codeml')

        parser.add_argument('--puppet_clt',
                        nargs = '?',
                        help = 'Input the codeml control file which instructs codeml analysis.',
                        type = str,
                        default = None)
        return vars(parser.parse_args())    
    
    pars = read_args(sys.argv)
    
    puppeteer_func(pars['puppet_tool'], pars['puppet_clt'])
    