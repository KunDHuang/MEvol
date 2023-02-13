#!/usr/bin/env python

import pandas as pd
from scipy.stats import ranksums, f_oneway, pearsonr
import sys
from statsmodels.sandbox.stats.multicomp import multipletests
import subprocess
import argparse
import textwrap

"""
NAME: gene_snv_vareval.py
DESCRIPTION: gene_snv_vareval.py is a script to evaluate the significance of SNV variation for each gene using statistic test.
AUTHOR: Kun D. Huang
Date: 09.02.2023
"""


class GeneEval:
    """
    This object contains multiple instances of variation test.   
    """
    
    def __init__(self, gene_snv_df, md_var):
        # gene_snv_df: The dataframe which contains pairwise SNV rates specific to only one gene
        # md_var: the metadata variable to be assessed.
        self.gene_snv_df = gene_snv_df
        self.md_var = md_var
    
    def ranksums_test(self, ref_group, test_group):
        # ref_group: The reference group in the comparison
        # test_group: The test group in the comparison
        
        ref_snv = self.gene_snv_df[self.gene_snv_df[self.md_var] == ref_group]['snv_rate'].to_list()
        test_snv = self.gene_snv_df[self.gene_snv_df[self.md_var] == test_group]['snv_rate'].to_list()
        pvalue = ranksums(ref_snv, test_snv).pvalue
        return pvalue
    
    def oneway_anova_test(self, ref_group, test_group):
        # ref_group: The reference group in the comparison
        # test_group: The test group in the comparison
        
        ref_snv = self.gene_snv_df[self.gene_snv_df[self.md_var] == ref_group]['snv_rate'].to_list()
        test_snv = self.gene_snv_df[self.gene_snv_df[self.md_var] == test_group]['snv_rate'].to_list()
        pvalue = f_oneway(ref_snv, test_snv).pvalue
        return pvalue
    
    def person_cor_test(self):
        
        independent_var = self.gene_snv_df[self.md_var].to_list()
        independent_var = [abs(i) for i in independent_var]
        response_var = self.gene_snv_df['snv_rate'].to_list()
        
        cor_eff, pvalue = pearsonr(independent_var, response_var)
        
        return cor_eff, pvalue
     
def generate_combinations(snv_df, md_var, reference):
    # snv_df: the input SNV dataframe
    # reference: the reference factor
    # This function is to generate combinations for variance test.
    all_factors = list(set([l for i in snv_df[md_var] for l in i.split("$")]))
    
    combs = [reference + "$" + i for i in all_factors]
    ref_group = []
    test_group = []
    
    for comb in combs:
        factor1 , factor2 = comb.split("$")
        if factor1 == factor2:
            ref_group.append(comb)
        else:
            test_group.append(comb)
    return ref_group[0], *test_group
    
def eval_gene(gene, snv_concat_df, md_var, ref_factor = None, method = 'ranksums'):
    # genes_lst: a list of genes for assessment.
    # snv_concat_df: the concatnated dataframe containing pairwise SNV rates.
    # md_var: the metadata variable to be assessed.
    # ref_factor: the refenrence factor in md_var.
    # method: the stat method to compare groups.
    
    gene_df = snv_concat_df[snv_concat_df['entry_id'] == gene]
    eval_obj = GeneEval(gene_df, md_var)
    matrix = []
    if method == 'pearson':
        if ref_factor:
            sys.exit("It seems that you want to do correlation analysis, so you do not need to set a reference factor: just leave ref_factor = None.")   
        else:
            cor_eff, pvalue = eval_obj.person_cor_test()
            matrix.append([gene, cor_eff, pvalue])
            sub_df = pd.DataFrame(matrix, columns = ['gene', 'cor_eff', 'pvalue'])
    else:
        if ref_factor:
            combs = generate_combinations(snv_concat_df, md_var, ref_factor)
            ref_pair = combs[0]
            test_pairs = combs[1:]
            for test_pair in test_pairs:
                if method == 'ranksums':
                    pvalue = eval_obj.ranksums_test(ref_pair, test_pair)
                elif method == 'oneway_anova':
                    pvalue = eval_obj.oneway_anova_test(ref_pair, test_pair)
                matrix.append([gene, ref_pair, test_pair, pvalue])
            sub_df = pd.DataFrame(matrix, columns = ['gene', 'ref_group', 'test_group', 'pvalue'])
            
        else:
            sys.exit("To test categorical data, you need to specify the reference factor.")

    return sub_df
        
        
if __name__ == "__main__":
    def read_args(args):
    # This function is to parse arguments

        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                         description = textwrap.dedent('''\
                                         This program is to examine genes whose pairwise SNV rates are significantly different between groups
                                         '''),
                                        epilog = textwrap.dedent('''\
                                        examples:  
                                       '''))
        parser.add_argument('--snv_rate_file',
                        nargs = '?',
                        help = 'Input the dataframe of pairwise SNV rates of core genes from one species.',
                        type = str,
                        default = None)

        parser.add_argument('--variable',
                        nargs = '?',
                        help = 'Specify the variable of interest.',
                        type = str,
                        default = None)
        
        parser.add_argument('--ref_factor',
                        nargs = '?',
                        help = 'Specify the reference factor if the variable is categorical. Skip it if the variable is continous.',
                        type = str,
                        default = None)
        
        parser.add_argument('--test_method',
                        nargs = '?',
                        help = 'Specify the stats method you want to use for testing significance.[ranksums/oneway_anova/pearson].',
                        type = str,
                        default = 'ranksums')
        
        parser.add_argument('--output',
                        nargs = '?',
                        help = 'Specify the output file name.',
                        type = str,
                        default = None)
        
        return vars(parser.parse_args())
    pars = read_args(sys.argv)
    
    snv_concat_df = pd.read_csv(pars["snv_rate_file"], sep = '\t', index_col = False)
    genes = list(set(snv_concat_df['entry_id']))
    genes_pvalue_dfs = [eval_gene(gene, snv_concat_df, pars['variable'], ref_factor = pars['ref_factor'], method = pars['test_method']) for gene in genes]
    concat_df = pd.concat(genes_pvalue_dfs)
    concat_df['fdr'] = multipletests(concat_df['pvalue'], alpha= 0.05, method='fdr_bh')[1]
    concat_df = concat_df[concat_df['fdr'] <= 0.05]
    concat_df.to_csv(pars['output'], sep = '\t', index = False)

