# MEvol: Original name finder

## Table of Contents
- [Introduction](#introduction)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Syntax](#syntax)


## Introduction
The `original_name_finder.py` script is designed to enhance your multiple sequence alignment files by replacing gene names with their corresponding genome names from the **[Roary](https://github.com/sanger-pathogens/Roary#introduction)** tool.

## How It Works
The script takes the following steps to improve your sequence alignment files that will be used for other downstream analyses:

1. **Utilization of Roary Output:** The script utilizes genome names from Roary's output, where genes are categorized by their respective bacterial species.

2. **Replacement of Gene Family Identifier:** For each gene family in the alignment file, the script substitutes the generic name with the corresponding genome name from Roary.

## Getting Started

### Prerequisites
Before you begin, make sure you have the following items:

1. **Gene Presence and Absence Table (`GENE_TABLE`):**
Obtain the Roary-generated gene presence and absence table in CSV format (`gene_presence_absence.csv`) for your dataset.

2. **Gene Family Alignment Directory (`GENE_FAMILY_DIR`):**
Prepare a directory containing the multiple sequence alignment files of gene families, sourced from Roary's `pan_genome_sequences` output. These files should ideally adhere to a consistent naming pattern.

### Syntax
```bash
MEVOL_DIR=/path/to/MEvol/directory
C_DIR=/path/to/working/directory

${MEVOL_DIR}/utils/original_name_finder.py \
--gene_family_dir ${C_DIR}/gene_family_alignments/ \
--gene_table ${C_DIR}/gene_presence_absence.csv \
--opt_dir ${C_DIR}/ori_name_msa/ \
--nproc 20
```

### Explaination

**`${MEVOL_DIR}`:** The path to the directory where the `original_name_finder.py` script is located.

**`${C_DIR}`:** The path to the working directory where your data and outputs are stored.

`--gene_family_dir`: Path to the directory containing gene family alignment files.
`--gene_table`: Path to the gene presence and absence table.
`--opt_dir`: Path to the output directory to store gene families with original sample names.
`--nproc`: The number of processes to use during execution.


**Note:** Please change `/path/to/` with the specific paths relevant to your system configuration. Additionally, make sure to customize the other paths to match the actual items or destinations required by your setup.






