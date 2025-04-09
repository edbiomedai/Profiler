from argparse import Namespace
from logging import Logger
import os
import pandas as pd

def merge_data(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Merging morphological data")
    areashape_dir = os.path.join(paths["data_staged"], "areashape.csv")
    intensity_dir = os.path.join(paths["data_staged"], "intensity.csv")
    spatial_dir = os.path.join(paths["data_staged"], "spatial.csv")
    qc_dir = os.path.join(paths["data_staged"], "qc.csv")
    out_dir = os.path.join(paths["data"], "morphology.csv")
    areashape_data = pd.read_csv(areashape_dir)
    intensity_data = pd.read_csv(intensity_dir)
    spatial_data = pd.read_csv(spatial_dir)
    qc_data = pd.read_csv(qc_dir)
    data_temp = pd.merge(areashape_data, intensity_data, how="left", on="Meta_Global_Mask_Label") 
    data_temp2 = pd.merge(data_temp, qc_data, how="left", on="Meta_Global_Mask_Label")
    data = pd.merge(data_temp2, spatial_data, how="left", on="Meta_Global_Mask_Label")
    data.to_csv(out_dir, index=False)
    logger.info("COMPLETED: Merging morphological data")