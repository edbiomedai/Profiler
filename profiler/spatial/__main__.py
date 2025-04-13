from ._spatial_calcs import calculate_local_counts, calculate_local_means, save_dist_mat

from argparse import ArgumentParser, Namespace
import dask.dataframe as dd
from functools import reduce
from glob import glob
import pandas as pd
from pathlib import Path
import os
from shutil import rmtree

def get_cli_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--input-folder", help="Input folder", type=str, required=True)
    return parser.parse_args()

if __name__=="__main__":
    args = get_cli_args()
    full_path = str(Path(args.input_folder).resolve())
    out_folder = os.path.join(full_path, "spatialstaged")
    out_dist_mat = os.path.join(out_folder, "dist_mat")
    os.mkdir(out_folder)
    data_file_path = os.path.join(full_path, "morphology.csv")
    data = dd.read_csv(data_file_path)
    save_dist_mat(data, out_dist_mat)

