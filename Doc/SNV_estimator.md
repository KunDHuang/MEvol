# MEvol: SNV estimator

## Table of Contents
- [Introduction](#introduction)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Syntax](#syntax)


## Introduction
The `snv_estimator.py` script is a powerful and adaptable tool designed to facilitate the thorough analysis of pairwise Single Nucleotide Variant (SNV) rates within a species' pangenome. 

With a diverse array of functionalities, the script excels in aiding the exploration of SNV patterns by offering the following features:

1. **Metadata Integration:** Users can append metadata to the estimated SNV rates. Metadata can be in character form, which is combined using `$`, or numeric form, which is presented as differences (e.g., seq1 - seq2).

2. **SNV Rate estimation:** The script estimates pairwise SNV rates for gene alignments.


## How It Works
1. Calculate SNV rates for all pairs of sequences in the input FASTA file.
2. Optionally, read and clean (select or remove) metadata from the provided metadata file.
3. For each SNV rate entry, fetch corresponding metadata for the sequences. Append metadata to the SNV rate entry.

## Getting Started

### Prerequisites
Before you begin, make sure you have the following items:

1. **Gene of Interest in Multiple Sequence Alignment (MSA) Fasta:**
Gather your gene family alignments in a directory. These alignments should originate from Roary's pan_genome_sequences output. Ensure the alignment files follow a consistent sample naming convention for easy processing.

2. **Metadata:**
The provided metadata, whether in categorical or numeric form, will be utilized for estimating pairwise SNV rates. This integration of metadata will enhance the accuracy and depth of the SNV rate estimation process.

### Syntax
```bash
MEVOL_DIR=/path/to/MEvol/directory
C_DIR=/path/to/working/directory

${MEVOL_DIR}/utils/snv_estimator.py \
--fasta ${C_DIR}/input_sequences.fa.aln \
--metadata ${C_DIR}/metadata_file.tsv \
--entry_col "entry_feature" \
--cols_kept_o_rm k,Metadata_feature1 \
# k: Feature to keep; r: Feature to remove
--opt_tab ${C_DIR}/output_directory/snv_rates_output.tsv \

```

### Explaination

**`${MEVOL_DIR}`:** The path to the directory where the `snv_estimator.py` script is located.

**`${C_DIR}`:** The path to the working directory where your data and outputs are stored.

`--fasta`: Path to the aligned FASTA file of input sequences.
`--metadata`: Path to the metadata file.
`--entry_col`: Feature nam.
`--cols_kept_o_rm`: Feature to keep (k) or remove (r) from metadata.
`--opt_tab`: Path to the output table to store SNV rates.


**Note:** Replace `/path/to/` with the actual paths in your setup and customize `Metadata_feature1` to the actual name of the metadata feature you want to keep or remove.

