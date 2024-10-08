# MEvol: Gene SNV Analyzer

!!! * ADD SOME FIGURE


## Table of Contents
- [Introduction](#introduction)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Syntax](#syntax)
  - [Explaination](#explaination)
- [Example: SNV Rate Estimation](#example-snv-rate-estimation)
   - [Output](#output)

## Introduction
The `snv_analyzer.py` script is a powerful and adaptable tool designed to facilitate the thorough analysis of pairwise Single Nucleotide Variant (SNV) rates within a species' pangenome. 

With a diverse array of functionalities, the script excels in aiding the exploration of SNV patterns by offering the following features:

1. **Gene Name Replacement:** The script replaces generic gene names in multiple sequence alignments with the corresponding genome names, enhancing alignment files' clarity and interpretability.

2. **Metadata Integration:** Users can append metadata to the estimated SNV rates. Metadata can be in character form, which is combined using `$`, or numeric form, which is presented as differences (e.g., feature1 - feature2).

3. **SNV Rate estimation:** The script estimates pairwise SNV rates for gene alignments.


## How It Works

1. **Finding Original Sample Names**:
   Before estimating SNV rates, the script utilizes the **[original_name_finder.py](./original_name_finder.md)** tool to identify the original sample names within the Multiple Sequence Alignment (MSA) pangenome sequences. This step ensures accurate identification and alignment of sequences during the SNV rate calculation.

2. **SNV Rate Estimation**:
   Once the original sample names are identified, the script proceeds to calculate the SNV rate for every gene in the MSA pangenome utilizing **[snv_estimator.py](./SNV_estimator.md)**. For each gene, it compares the aligned sequences and counts the SNV, allowing for a comprehensive assessment of genetic diversity and variation within the dataset.

3. **Metadata Integration**:
   For a more comprehensive analysis, the script offers the option to include metadata associated with the sequences. Metadata should provide additional context and information about the pairwise comparison (i.e., Diet, BMI, or score).

4. **Output Generation and Saving**:
   After estimating SNV rates and incorporating metadata, the script generates a final DataFrame that includes SNV rates, SNV counts, gap ratios, and any appended metadata. This DataFrame captures a comprehensive snapshot of the genetic variations within the aligned sequences, coupled with relevant contextual information.


## Getting Started

### Prerequisites
Before you begin, make sure you have the following items:

1. **Gene Presence and Absence Table:**
   Obtain the gene presence and absence table generated by Roary, which should be in CSV format named `gene_presence_absence.csv`. This table serves as the reference for gene families in your dataset.

2. **Gene Family Alignment Directory:**
   Prepare a directory containing the MSA files of gene families. These alignments are typically derived from Roary's `pan_genome_sequences` output. Ensure that the MSA files follow a consistent naming pattern for easy identification.

3. **Metadata:**
   If you have metadata associated with your sequences, ensure you have a metadata file ready. Metadata can be in categorical or numeric format. Metadata provides context and additional information about the sequences, such as species, diet, or other relevant variables.


### Syntax
```bash
MEVOL_DIR=/path/to/MEvol/directory
C_DIR=/path/to/working/directory

${MEVOL_DIR}/gene_snv_analyzer.py \
--gene_family_dir ${C_DIR}/gene_family_alignments/ \
--gene_table ${C_DIR}/gene_presence_absence.csv \
--metadata ${C_DIR}/metadata_file.tsv \
--opt_dir ${C_DIR}/output_directory/ \
--concat_tab ${C_DIR}/output_directory/ concatenated_table.tsv \
--cols_kept_o_rm k,Metadata_feature1 \
--nproc 5 \
--coreness 63 
```
### Explaination
This script snippet demonstrates how to use the gene_snv_analyzer.py script with the provided arguments. Here's a breakdown of each argument:

**`${MEVOL_DIR}`:** The path to the directory where the `gene_snv_analyzer.py` script is located.

**`${C_DIR}`:** The path to the working directory where your data and outputs are stored.

`--gene_family_dir`: Path to the directory containing gene family alignment files.
`--gene_table`: Path to the gene presence and absence table in CSV format.
`--metadata`: Path to the metadata file.
`--opt_dir`: Path to the directory where output files will be saved.
`--concat_tab`: Path to the concatenated output table.
`--cols_kept_o_rm`: A flag (k or r) followed by a comma-separated list of metadata feature to keep or remove.
`--nproc`: The number of processes to use during execution.
`--coreness`: Specifies the number of coreness. If not specified, the coreness will be automatically estimated by default.

**Note:** Replace `/path/to/` with the actual paths in your setup and customize `Metadata_feature1` to the actual name of the metadata feature you want to keep or remove.

_______________________________
## Example: SNV Rate Estimation
In this section, we'll walk through practical examples of using the `snv_estimator.py` script to estimate pairwise SNV rates for gene families and incorporate metadata. These examples will showcase how to adapt the script to different scenarios and data configurations.

##### Demo
```bash
conda activate MEvol
unset PYTHONPATH

MEVOL_DIR=./MEvol

C_DIR=./demo

${MEVOL_DIR}/gene_snv_analyzer.py \
--gene_family_dir ${C_DIR}/demo/gene_fam/ \
--metadata ${C_DIR}/demo/mag_metadata.tsv \
--cols_kept_o_rm k,Diet \
--nproc 5 \
--gene_table ${C_DIR}/demo/gene_presence_absence.csv \
--opt_dir ${C_DIR}/demo/outdir/ \
--concat_tab concat_snv_rates.tsv
```

### Output
Upon running the `gene_snv_analyzer.py` script, you can expect the following output files:

- **`snv_rate_files`:**
  This directory contains the estimated pairwise SNV rates for each gene family. Each gene family's SNV rates are stored in separate `.tsv` files.

- **`concat_snv_rates.tsv`:**
  A consolidated file containing the estimated pairwise SNV rates for all gene families. This file combines the SNV rates of all gene families into one comprehensive `.tsv` format.

- **`tmp*`:**
  Temporary directories name begin with `tmp*` store the gene families in MSA format (`.aln`). Each temporary directory corresponds to a specific sampleID's gene families. These temporary directories are used internally during the script's execution.

_______________________
## Example: SNV Evaluation
Once you have obtained the concat_snv_rates.tsv file, you're ready to perform rigorous statistical testing for SNV evaluation using the `gene_snv_vareval.py`. 

The `gene_snv_vareval.py` script empowers you to assess the significance of SNV rates in a pairwise manner. This analysis enables the identification of genes or genomic regions with substantial SNV rate variations, facilitating the discovery of potential genetic markers or signatures.

This section outlines the steps required to conduct comprehensive SNV analysis, enabling you to uncover meaningful insights from your data.

##### Syntax
```bash
MEVOL_DIR=/path/to/MEvol/directory
C_DIR=/path/to/working/directory

${MEVOL_DIR}/utils/gene_snv_vareval.py \
--snv_rate_file ${C_DIR}/concatenated_snv_rates.tsv \
--output ${C_DIR}/SNV_evaluation_results.tsv \
--variable Feature \
--ref_factor Reference_Feature \
--test_method Statistical_test [ranksums/oneway_anova/pearson]
```

##### Demo
```bash
conda activate MEvol
unset PYTHONPATH

MEVOL_DIR=./MEvol

C_DIR=./demo

${MEVOL_DIR}/utils/gene_snv_vareval.py \
--snv_rate_file ${C_DIR}/demo/outdir/concat_snv_rates.tsv \
--output ${C_DIR}/demo/outdir/SNV_eval_vegan_ref.tsv \
--variable Diet \
--ref_factor Vegan \
--test_method ranksums 
```
### Output
Upon running the `gene_snv_vareval.py` script, you can expect the following output files:

- **`SNV_eval_vegan_ref.tsv`:**
This consolidated file presents the outcomes of statistical testing for SNV rates conducted in a pairwise manner between groups of interest.

____________________________________
##### Further Information 
1. [Roary](https://github.com/sanger-pathogens/Roary#introduction)
2. [Pan-genome](https://en.wikipedia.org/wiki/Pan-genome)

