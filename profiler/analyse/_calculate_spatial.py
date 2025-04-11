from argparse import Namespace
import dask.array as da
import dask.dataframe as dd
from logging import Logger
import os
import pandas as pd
from time import time

def calculate_local_counts(df: dd.DataFrame, distance_threshold: int = 25) -> dd.DataFrame:
    out_var = f"Spatial_Nuclei_Mask_LocalCount{distance_threshold}"
    data = df[["Meta_Global_Mask_Label", "Meta_Nuclei_Mask_CentroidY", "Meta_Nuclei_Mask_CentroidY"]]
    coords = data[["Meta_Nuclei_Mask_CentroidY", "Meta_Nuclei_Mask_CentroidY"]].to_dask_array(lengths = True)
    coords = coords.rechunk((4096, 2))
    x_diff = coords[:, None, 0] - coords[None, :, 0]
    y_diff = coords[:, None, 1] - coords[None, :, 1]
    dist_mat = da.less_equal(da.sqrt(x_diff ** 2 + y_diff ** 2), distance_threshold).astype(int)
    dist_mat[da.eye(dist_mat.shape[0], dtype=bool)] = 0
    data[out_var] = dist_mat.sum(axis=1).to_dask_dataframe().repartition(npartitions=data.npartitions)
    return data[["Meta_Global_Mask_Label", out_var]]

def calculate_local_means(df: dd.DataFrame, variable_name: str, distance_threshold: int = 25) -> dd.DataFrame:
    data = df[["Meta_Global_Mask_Label", "Meta_Nuclei_Mask_CentroidY", "Meta_Nuclei_Mask_CentroidY", variable_name]]
    coords = data[["Meta_Nuclei_Mask_CentroidY", "Meta_Nuclei_Mask_CentroidY"]].to_dask_array(lengths = True)
    coords = coords.rechunk((4096, 2))
    x_diff = coords[:, None, 0] - coords[None, :, 0]
    y_diff = coords[:, None, 1] - coords[None, :, 1]
    dist_mat = da.less_equal(da.sqrt(x_diff ** 2 + y_diff ** 2), distance_threshold).astype(int)
    dist_mat[da.eye(dist_mat.shape[0], dtype=bool)] = 0
    val_col = data[variable_name].to_dask_array(lengths=True).reshape(-1, 1)
    sum_mat = (da.tile(val_col, (1, val_col.shape[0])).rechunk((4096, 4096)) * dist_mat).sum(axis=1)
    count_mat = dist_mat.sum(axis=1)
    count_mat = da.where(count_mat < 1, 1, count_mat)
    avg_mat = sum_mat / count_mat
    out_var = f"Spatial_Nuclei_Mask_LocalAverage{variable_name.replace("_", "")}{distance_threshold}"
    data[out_var] = avg_mat.to_dask_dataframe().repartition(npartitions=data.npartitions)
    return data[["Meta_Global_Mask_Label", out_var]]


def calculate_spatial(args: Namespace, logger: Logger, paths: dict, benchmarks: dict):
    logger.info("STARTED: Calculating spatial data")
    start_time = time()
    mpdata_path = os.path.join(paths["data_staged"], "areashape.csv")
    indata_path = os.path.join(paths["data_staged"], "intensity.csv")
    out_dir = os.path.join(paths["data_staged"], "spatial.csv")
    mpdata = dd.read_csv(mpdata_path)
    indata = dd.read_csv(indata_path)
    data = dd.merge(mpdata, indata, how="left", on="Meta_Global_Mask_Label")
    spatial_df = calculate_local_counts(data)
    other_dfs = [
        calculate_local_means(data, "AreaShape_Nuclei_Mask_Area"),
        calculate_local_means(data, "AreaShape_Nuclei_Mask_Eccentricity"),
        calculate_local_means(data, "AreaShape_Nuclei_Mask_AxisMinorLength"),
        calculate_local_means(data, "AreaShape_Cell_Mask_Area")
    ]
    if args.stain_type == "IHC":
        other_dfs.append(calculate_local_means(data, "Intensity_Cytoplasm_DAB_MeanIntensity"))
    for df in other_dfs:
        spatial_df = dd.merge(spatial_df, df, how="left", on="Meta_Global_Mask_Label")
    spatial_df.to_csv(out_dir, index=False, single_file=True)
    end_time = time()
    benchmarks["spatial_calcs"] = end_time - start_time
    logger.info("COMPLETED: Calculating spatial data")
    