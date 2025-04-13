from ._spatial_calcs import calculate_local_counts, calculate_local_means

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
    os.mkdir(out_folder)
    data_file_path = os.path.join(full_path, "morphology.csv")
    data = dd.read_csv(data_file_path)
    calculate_local_counts(data, distance_threshold=25).to_csv(os.path.join(out_folder, "spatial_counts1.csv"), index=False)
    calculate_local_counts(data, distance_threshold=50).to_csv(os.path.join(out_folder, "spatial_counts2.csv"), index=False)
    calculate_local_counts(data, distance_threshold=75).to_csv(os.path.join(out_folder, "spatial_counts3.csv"), index=False)
    calculate_local_counts(data, distance_threshold=100).to_csv(os.path.join(out_folder, "spatial_counts4.csv"), index=False)
    calculate_local_means(data, "AreaShape_Nuclei_Mask_Area", distance_threshold=100).to_csv(os.path.join(out_folder, "spatial_means5.csv"), index=False)
    calculate_local_means(data, "AreaShape_Nuclei_Mask_AxisMinorLength", distance_threshold=100).to_csv(os.path.join(out_folder, "spatial_means6.csv"), index=False)
    calculate_local_means(data, "AreaShape_Nuclei_Mask_Eccentricity", distance_threshold=100).to_csv(os.path.join(out_folder, "spatial_means7.csv"), index=False)
    calculate_local_means(data, "Intensity_Cytoplasm_DAB_MeanIntensity", distance_threshold=100).to_csv(os.path.join(out_folder, "spatial_means8.csv"), index=False)
    spatial_data_files = glob(os.path.join(out_folder, "spatial_*"))
    spatial_data_dfs = [pd.read_csv(path) for path in spatial_data_files]
    spatial_df = reduce(lambda left, right: pd.merge(left, right, on="Meta_Global_Mask_Label", how="outer"), spatial_data_dfs)
    spatial_df.to_csv(os.path.join(full_path, "spatial.df"), index=False)
    rmtree(out_folder)

