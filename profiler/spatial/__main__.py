from ._spatial_window import create_spatial_windows

from argparse import ArgumentParser, Namespace
import dask.dataframe as dd
from glob import glob
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
    spatial_temp_path = os.path.join(full_path, "spatial_temp")
    os.mkdir(spatial_temp_path)
    spatial_windows_path = os.path.join(spatial_temp_path, "spatial_windows")
    os.mkdir(spatial_windows_path)
    local_counts_path = os.path.join(spatial_temp_path, "local_counts")
    data = dd.read_csv(os.path.join(full_path, "morphology.csv"))
    create_spatial_windows(data, spatial_windows_path)
    for i, spatial_window in enumerate(glob(os.path.join(spatial_windows_path, "*.csv"))):
        pass
