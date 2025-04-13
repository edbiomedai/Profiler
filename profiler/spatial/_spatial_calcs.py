import dask.array as da
import dask.dataframe as dd
import pandas as pd

def save_dist_mat(df: dd.DataFrame, path: str, distance_threshold: int = 100) -> None:
    data = df[["Meta_Global_Mask_Label", "Meta_Nuclei_Mask_CentroidX", "Meta_Nuclei_Mask_CentroidY"]]
    coords = data[["Meta_Nuclei_Mask_CentroidX", "Meta_Nuclei_Mask_CentroidY"]].to_dask_array(lengths = True)
    coords = coords.rechunk((2048, 2))
    x_diff = coords[:, None, 0] - coords[None, :, 0]
    y_diff = coords[:, None, 1] - coords[None, :, 1]
    dist_mat = da.sqrt(x_diff ** 2 + y_diff ** 2)
    threshold_dist_mat = da.less_equal(dist_mat, distance_threshold)
    threshold_dist_mat[da.eye(threshold_dist_mat.shape[0], dtype=bool)] = False
    threshold_dist_mat.to_zarr(path)

def calculate_local_counts(dist_mat: da.Array, distance_threshold: int = 25) -> dd.DataFrame:
    out_var = f"Spatial_Nuclei_Mask_LocalCount{distance_threshold}"
    return dd.from_dask_array(dist_mat.sum(axis=1), columns=out_var)

def calculate_local_means(df: dd.DataFrame, var_name: str, distance_threshold: int = 25) -> dd.DataFrame:
    out_var = f"Spatial_Nuclei_Mask_LocalAvg{var_name.replace("_", "")}{distance_threshold}"
    data = df[["Meta_Global_Mask_Label", "Meta_Nuclei_Mask_CentroidX", "Meta_Nuclei_Mask_CentroidY", var_name]]
    coords = data[["Meta_Nuclei_Mask_CentroidX", "Meta_Nuclei_Mask_CentroidY"]].to_dask_array(lengths = True)
    coords = coords.rechunk((2048, 2))
    x_diff = coords[:, None, 0] - coords[None, :, 0]
    y_diff = coords[:, None, 1] - coords[None, :, 1]
    dist_mat = da.less_equal(da.sqrt(x_diff ** 2 + y_diff ** 2), distance_threshold).astype(int).rechunk(2048, 2048)
    dist_mat[da.eye(dist_mat.shape[0], dtype=bool)] = 0
    val_mat = data[[var_name]].to_dask_array(lengths=True).reshape(-1, 1)
    val_mat = da.tile(val_mat, (1, val_mat.shape[0])).rechunk((2048, 2048))
    val_mat = val_mat * dist_mat
    counts = dist_mat.sum(axis=1)
    counts = da.where(counts < 1, 1, counts)
    sums = val_mat.sum(axis=1)
    avgs = sums/counts
    return dd.from_dask_array(avgs, columns=out_var)