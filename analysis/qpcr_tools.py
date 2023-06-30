# Tools for loading and manipulating qPCR data
# Author: Felix Horns
# Date created: 6/14/2021
# Copyright Felix Horns 2021

import glob
import pandas as pd


def load_qPCR_from_dir_Cq(infiles_dir, infile=None, plate_id=""):
    """ Loads Cq results. Finds name of Cq file within input directory, unless input file is specified.
        Annotates file with plate identifier (plate_id). Returns Pandas dataframe. """

    # Find name of input file
    if infile is None:

        matches = glob.glob(infiles_dir + "/* Quantification Cq Results.csv")

        if len(matches) > 1:
            print('Warning: more than one file within input directory infiles_dir matched pattern for "Quantification Cq Results.csv". Using first match.')

        infile = matches[0]

    # Load dataframe
    result = pd.read_csv(infile, header=0)

    # Drop useless columns
    columns_to_drop = ["Unnamed: 0", "Well Note"]
    for col in columns_to_drop:
        if col in result.columns:
            result.drop(col, axis=1, inplace=True)

    # Set plate identifier
    result["Plate"] = plate_id
    
    # Set index to well identifier
    result.set_index("Well", inplace=True)

    return result


def load_qPCR_from_dir_Amplification_SYBR(infiles_dir, infile=None):
    """ Loads amplification traces. Finds name of input file within input directory, unless input file is specified.
        Returns Pandas dataframe. """

    # Find name of input file
    if infile is None:

        matches = glob.glob(infiles_dir + "/* Quantification Amplification Results_SYBR.csv")

        if len(matches) > 1:
            print('Warning: more than one file within input directory infiles_dir matched pattern for "Quantification Amplification Results_SYBR.csv". Using first match.')
            
        infile = matches[0]
    
    # Load dataframe
    result = pd.read_csv(infile, header=0)

    # Drop useless columns
    columns_to_drop = ["Unnamed: 0"]
    result.drop(columns_to_drop, axis=1, inplace=True)

    return result


def load_qPCR_from_dir_Standard_Curve(infiles_dir, infile=None):
    """ Loads standard curve summary. Finds name of input file within input directory, unless input file is specified.
        Annotates file with plate identifier (plate_id). Returns Pandas dataframe. """

    # Find name of input file
    if infile is None:

        matches = glob.glob(infiles_dir + "/* Standard Curve Results.csv")

        if len(matches) > 1:
            print('Warning: more than one file within input directory infiles_dir matched pattern for "Quantification Amplification Results_SYBR.csv". Using first match.')
            
        infile = matches[0]
    
    # Load dataframe
    result = pd.read_csv(infile, header=0)

    # Drop useless columns
    columns_to_drop = ["Unnamed: 0"]
    result.drop(columns_to_drop, axis=1, inplace=True)

    return result
    

def load_qPCR_from_dir(infiles_dir, plate_id=""):
    """ Loads Cq, amplification traces, and standard curve summary. Wrapper for functions that load each item. 
        Returns tuple of Pandas dataframes. """

    Cq = load_qPCR_from_dir_Cq(infiles_dir, plate_id=plate_id)
    amp = load_qPCR_from_dir_Amplification_SYBR(infiles_dir)
    std = load_qPCR_from_dir_Standard_Curve(infiles_dir)

    return Cq, amp, std


def concat_dfs_Cq(dfs):
    """ Concatentate dataframes of Cq. """

    # Reset index so Well field becomes a column
    dfs_reset = []
    for df in dfs:
        dfs_reset.append(df.reset_index())  # make a copy of each df so that original is not touched

    # Concatenate
    result = pd.concat(dfs_reset)

    return result


def load_metadata(infile):
    """ Load metadata csv. """
    result = pd.read_csv(infile, header=0)
    return result


def select_amp_std(amp, quant):
    """ Select subset of amplification traces related to standards. 
        Input is:
        1) dataframe of amplification traces (e.g. such as loaded by load_qPCR_from_dir_Amplification_SYBR()),
        with columns indexed by Well.
        2) dataframe containing metadata specifying the content of each well, such as the Cq dataframe
        loaded by load_qPCR_from_dir_Cq(), indexed by Well.
        Output is a subset of rows of the dataframe, identified by Content column containing the substring 'Std-'. """

    subset_index = quant.loc[quant.Content.str.contains("Std-")].index  # select rows containing standards
    subset_index_clean = subset_index.str.replace("0", "")  # remove zeros in index, to conform to standard in Amplification dataframe column labels (which has no zeros).
    subset_index_clean = list(set(subset_index_clean) & set(amp.columns))  # take intersection to get wells that are actually present in amplification traces dataframe.

    return amp[subset_index_clean]


def select_quant_std(quant):
    """ Select subset of Cq rows related to standards.
        Input is dataframe of Cq values, such as loaded by load_qPCR_from_dir_Cq().
        Output is a subset of rows of the dataframe, identified by Content column containing the substring 'Std-'. """
    subset_index = quant.loc[quant.Content.str.contains("Std-")].index  # select rows containing standards
    return quant.loc[subset_index]


def select_quant_summary_samples_ordered(quant_summary, quant, samples_ordered, key="Sample"):
    """ Select samples in desired order.
        Select rows in quant_summary based on index (which is assumed to be "Sample" by default).
        Select rows in quant based on column specified by key, which is "Sample" by default.
        Return selected rows in quant and quant_summary in the desired order. """

    quant_summary_subset = quant_summary.loc[samples_ordered]  # select subset of wells in desired order

    # Select rows in quant based on column key
    selector = quant[key].isin(samples_ordered)
    quant_subset = quant.loc[selector]

    # Sort rows in quant based on desired order
    quant_subset = quant_subset.copy()  # make a copy of quant, so original is not changed
    quant_subset[key] = pd.Categorical(quant_subset[key], samples_ordered)  # set Sample as categorical, so it can be sorted in a custom order (specified by order in samples_ordered)
    quant_subset.sort_values(key, inplace=True)  # sort by Sample

    return quant_summary_subset, quant_subset

    



