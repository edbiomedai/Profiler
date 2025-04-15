from ._spatial_calcs import calculate_local_counts
from ._spatial_window import create_spatial_windows

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

def concat_dfs(in_dir: str, out_path: str) -> None:
    paths = glob(os.path.join(in_dir, "*.csv"))
    dfs = [pd.read_csv(path) for path in paths]
    df = pd.concat(dfs, axis=0)
    df.to_csv(out_path, index=False)

if __name__=="__main__":
    args = get_cli_args()
    full_path = str(Path(args.input_folder).resolve())
    spatial_temp_path = os.path.join(full_path, "spatial_temp")
    os.mkdir(spatial_temp_path)
    spatial_windows_path = os.path.join(spatial_temp_path, "spatial_windows")
    os.mkdir(spatial_windows_path)
    data = dd.read_csv(os.path.join(full_path, "morphology.csv"))
    create_spatial_windows(data, spatial_windows_path)
    local_counts_path_25 = os.path.join(spatial_temp_path, "local_counts_25")
    local_counts_path_50 = os.path.join(spatial_temp_path, "local_counts_50")
    local_counts_path_75 = os.path.join(spatial_temp_path, "local_counts_75")
    local_counts_path_100 = os.path.join(spatial_temp_path, "local_counts_100")
    local_counts_path_125 = os.path.join(spatial_temp_path, "local_counts_125")
    local_counts_path_150 = os.path.join(spatial_temp_path, "local_counts_150")
    local_counts_path_175 = os.path.join(spatial_temp_path, "local_counts_175")
    local_counts_path_200 = os.path.join(spatial_temp_path, "local_counts_200")
    os.mkdir(local_counts_path_25)
    os.mkdir(local_counts_path_50)
    os.mkdir(local_counts_path_75)
    os.mkdir(local_counts_path_100)
    os.mkdir(local_counts_path_125)
    os.mkdir(local_counts_path_150)
    os.mkdir(local_counts_path_175)
    os.mkdir(local_counts_path_200)
    spatial_window_dfs = [pd.read_csv(path) for path in glob(os.path.join(spatial_windows_path, "*.csv"))]
    for i, window in enumerate(spatial_window_dfs):
        calculate_local_counts(window, os.path.join(local_counts_path_25, f"local_counts{i}.csv"), distance_threshold=25)
        calculate_local_counts(window, os.path.join(local_counts_path_50, f"local_counts{i}.csv"), distance_threshold=50)
        calculate_local_counts(window, os.path.join(local_counts_path_75, f"local_counts{i}.csv"), distance_threshold=75)
        calculate_local_counts(window, os.path.join(local_counts_path_100, f"local_counts{i}.csv"), distance_threshold=100)
        calculate_local_counts(window, os.path.join(local_counts_path_100, f"local_counts{i}.csv"), distance_threshold=125)
        calculate_local_counts(window, os.path.join(local_counts_path_100, f"local_counts{i}.csv"), distance_threshold=150)
        calculate_local_counts(window, os.path.join(local_counts_path_100, f"local_counts{i}.csv"), distance_threshold=175)
        calculate_local_counts(window, os.path.join(local_counts_path_100, f"local_counts{i}.csv"), distance_threshold=200)
    concat_dfs(local_counts_path_25, os.path.join(spatial_temp_path, "local_counts_25.csv"))
    concat_dfs(local_counts_path_50, os.path.join(spatial_temp_path, "local_counts_50.csv"))
    concat_dfs(local_counts_path_75, os.path.join(spatial_temp_path, "local_counts_75.csv"))
    concat_dfs(local_counts_path_100, os.path.join(spatial_temp_path, "local_counts_100.csv"))
    concat_dfs(local_counts_path_125, os.path.join(spatial_temp_path, "local_counts_125.csv"))
    concat_dfs(local_counts_path_150, os.path.join(spatial_temp_path, "local_counts_150.csv"))
    concat_dfs(local_counts_path_175, os.path.join(spatial_temp_path, "local_counts_175.csv"))
    concat_dfs(local_counts_path_200, os.path.join(spatial_temp_path, "local_counts_200.csv"))
    spatial_dfs = glob(os.path.join(spatial_temp_path, "*.csv"))
    spatial_dfs = [pd.read_csv(path) for path in spatial_dfs]
    out_df = reduce(lambda left, right: pd.merge(left, right, on="Meta_Global_Mask_Label", how='left'), spatial_dfs)
    out_df.to_csv(os.path.join(full_path, "spatial.csv"), index=False)
    rmtree(spatial_temp_path)
        
