import numpy as np
import pandas as pd

def calculate_local_counts(df: pd.DataFrame, path: str, distance_threshold: int = 200) -> None:
    coords = df[["Meta_Nuclei_Mask_CentroidX", "Meta_Nuclei_Mask_CentroidY"]].values
    x_diff = coords[:, None, 0] - coords[None, :, 0]
    y_diff = coords[:, None, 1] - coords[None, :, 1]
    dist_mat = np.sqrt(x_diff ** 2 + y_diff ** 2)
    thresh_dist_mat = dist_mat < distance_threshold
    np.fill_diagonal(thresh_dist_mat, False)
    counts = thresh_dist_mat.astype(int).sum(axis=1)
    out_df = pd.DataFrame({"Meta_Global_Mask_Label": df["Meta_Global_Mask_Label"], f"Spatial_Nuclei_Spatial_LocalCounts{distance_threshold}": counts, 'InRegion': df["InRegion"]})
    out_df = out_df[out_df["InRegion"]]
    out_df[["Meta_Global_Mask_Label", f"Spatial_Nuclei_Spatial_LocalCounts{distance_threshold}"]].to_csv(path, index=False)