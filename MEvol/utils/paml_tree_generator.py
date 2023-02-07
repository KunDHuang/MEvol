#!/usr/bin/env python

from ete3 import Tree
import math
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

def paml_msa_parser(paml_msa):
    # paml_msa: the multiple sequence alignment in PAML format.
    # This function is to parse a PAML file into a SeqRecord structure.
    paml_list = open(paml_msa).read().rstrip().split("\n")
    seq_nr, seq_len = [i for i in paml_list[0].split(" ") if len(i) > 0]
    seq_nr = int(seq_nr)
    paml_list = paml_list[1:]
    step = math.ceil(float(seq_len)/60) + 1
    chunks = [paml_list[x: x + step] for x in range(0, len(paml_list), step)]
    seqrecords = []
    for chunk in chunks:
        seqrecords.append(SeqRecord(seq = Seq("".join(chunk[1:])),
                                    id = chunk[0],
                                    name = chunk[0],
                                    description = chunk[0]))
    
    return seqrecords
        

def relabel_tree(paml_msa, best_tree):
    
    tree_leafs = [seq_rec.id for seq_rec in paml_msa_parser(paml_msa)]
    tree_leaf_numbers = {leaf: tree_leafs.index(leaf) + 1 for leaf in tree_leafs}
    
    core_tree = Tree(open(best_tree).read().rstrip(), format = 0)
    for node in core_tree.traverse("postorder"):
        if node.name in tree_leaf_numbers:
            node.name = tree_leaf_numbers[node.name]

    core_tree.write(format = 9, outfile = "tree_nr_test.txt")












if __name__ == "__main__":
    relabel_tree("dusC.paml", "../RAxML_bestTree.Anaerobutyricum_hallii")
