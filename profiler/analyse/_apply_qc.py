from argparse import Namespace
import dask.dataframe as dd
from logging import Logger
import os
import zarr

def apply_qc_block(df, a):
    ys = df["Meta_Nuclei_Mask_CentroidY"]
    xs = df["Meta_Nuclei_Mask_CentroidX"]
    vs = []
    for y, x in zip(ys, xs):
        yi = int(y/32)
        xi = int(x/32)
        vs.append(a[yi,xi])
    df.loc[:, "QC_Global_Mask_SegVal"] = vs
    return df

def apply_qc(args: Namespace, logger: Logger, paths: dict, benchmarks: dict):
    logger.info("STARTED: Profiling area and shape morphology")
    qcmask_path = os.path.join(paths["mask_qc"], "mask_qc.zarr")
    mpdata_path = os.path.join(paths["data_staged"], "areashape.csv")
    out_dir = os.path.join(paths["data_staged"], "qc.csv")
    mpdata_full = dd.read_csv(mpdata_path).repartition(npartitions=100)
    mpdata = mpdata_full[["Meta_Global_Mask_Label", "Meta_Nuclei_Mask_CentroidY", "Meta_Nuclei_Mask_CentroidX"]]
    qcmask = zarr.open(qcmask_path)[:]
    qcdata = mpdata.map_partitions(lambda x: apply_qc_block(x, qcmask))[['Meta_Global_Mask_Label', 'QC_Global_Mask_SegVal']]
    qcdata.to_csv(out_dir, index=False, single_file=True)
    logger.info("COMPLETED: Profiling area and shape morphology")