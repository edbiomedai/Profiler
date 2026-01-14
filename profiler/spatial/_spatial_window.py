import dask.dataframe as dd
import os
from pathlib import Path

KEEP_COLS = [
    "Meta_Global_Mask_Label",
    "Meta_Nuclei_Mask_CentroidY",
    "Meta_Nuclei_Mask_CentroidX",
    "AreaShape_Nuclei_Mask_Area",
    "AreaShape_Nuclei_Mask_AxisMinorLength",
    "AreaShape_Nuclei_Mask_Eccentricity",
    "Intensity_Cytoplasm_Secondary_MeanIntensity",
    "Intensity_Cytoplasm_Secondary_MedianIntensity"
]

def create_spatial_windows(df: dd.DataFrame, path: str, window_size:  int = 3000, overlap: int = 400) -> None:
    path = str(Path(path).resolve())
    ymax = int(df["Meta_Nuclei_Mask_CentroidY"].max().compute()) + 1
    xmax = int(df["Meta_Nuclei_Mask_CentroidX"].max().compute()) + 1
    i = 0
    for y_seed in range(0, ymax, window_size):
        for x_seed in range(0, xmax, window_size):
            temp_data = df[(
                (df["Meta_Nuclei_Mask_CentroidY"] > y_seed - overlap) &
                (df["Meta_Nuclei_Mask_CentroidY"] < y_seed + window_size + overlap) &
                (df["Meta_Nuclei_Mask_CentroidX"] > x_seed - overlap) &
                (df["Meta_Nuclei_Mask_CentroidX"] < x_seed + window_size + overlap)
            )]
            temp_data = temp_data[KEEP_COLS].compute()
            temp_data["InRegion"] = (
                (temp_data["Meta_Nuclei_Mask_CentroidY"] > y_seed) &
                (temp_data["Meta_Nuclei_Mask_CentroidY"] < y_seed + window_size) &
                (temp_data["Meta_Nuclei_Mask_CentroidX"] > x_seed) &
                (temp_data["Meta_Nuclei_Mask_CentroidX"] < x_seed + window_size)
            )
            if len(temp_data[temp_data["InRegion"]]) > 0:
                if len(temp_data) > 1:
                    temp_data.to_csv(os.path.join(path, f"spatial{i}.csv"), index=False)
                    i += 1