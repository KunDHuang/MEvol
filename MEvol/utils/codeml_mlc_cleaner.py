#!/usr/bin/env python

import pandas as pd
import sys
import argparse
import textwrap

"""
NAME: codeml_mlc_cleaner.py
DESCRIPTION: codeml_mlc_cleaner.py is a python script to clean a concatenated file which contains
             lots of genes' adaptive evolution results.
AUTHOR: Kun D. Huang
DATE: 16.03.2023 
"""

def mlc_cleaner(concat_mlc_df, models):
    # concat_mlc_df: the concatenated dataframe containing omega estimates for many genes.
    # models: a list of model names one would like to focus on.
    # This function is to remove those genes whose significance for specified models are not qualified.
    all_entries = list(set(concat_mlc_df['id'].to_list()))
    sel_entries = []
    for entry in all_entries:
        df_entry = concat_mlc_df[concat_mlc_df['id'] == entry]
        flag_list = []
        for model in models:
            df_entry_model = df_entry[df_entry['model'] == model]
            flag_list.extend(df_entry_model['chi2_sig'].to_list())
        flag = list(set(flag_list))
        if flag.count(1) == 1 and len(flag) == 1:
            sel_entries.append(entry)
    
    df_ = concat_mlc_df[concat_mlc_df['id'].isin(sel_entries)]
    return df_
    

if __name__ == "__main__":
    
    def read_args(args):
    # This function is to parse arguments

        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description = textwrap.dedent('''\
                                         This program is to clean the concatenated codeml mlc file.
                                         '''),
                                         epilog = textwrap.dedent('''\
                                         examples: codeml_mlc_cleaner.py --codeml_mlc [codeml_mlc] --output [cleaned_codeml_mlc]
                                         '''))
        parser.add_argument('--codeml_mlc',
                        nargs = '?',
                        help = 'Input the concatenated mlc file.',
                        type = str,
                        default = None)

        parser.add_argument('--models',
                        nargs = '?',
                        help = 'Specify the models you want to focus on [M01] or [M12] or [M01,M12]. Default: M01,M12',
                        type = str,
                        default = "M01,M12")
        
        parser.add_argument('--output',
                        nargs = '?',
                        help = 'Specify the output file name.',
                        type = str,
                        default = None)

        return vars(parser.parse_args())
    
    pars = read_args(sys.argv)

    mlc_file = pd.read_csv(pars["codeml_mlc"], sep = "\t", index_col = False)
    models = pars["models"].split(",")
    cleaned_mlc_file = mlc_cleaner(mlc_file, models)
    cleaned_mlc_file.to_csv(pars["output"], sep = "\t", index = False)