from argparse import Namespace
import dask.array as da
from dask_image.ndmeasure import label
from dask_image.ndmorph import binary_erosion
from logging import Logger
import os
from scematk.io import read_zarr_bin_mask
from skimage.morphology import disk
from time import time

def create_qc_mask(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Generating QC Mask")
    tis_mask_dir = paths["mask_tissue"]
    tis_mask_zarr = os.path.join(tis_mask_dir, "img.zarr")
    tis_mask_meta = os.path.join(tis_mask_dir, "meta.json")
    tissue_mask_scematk = read_zarr_bin_mask(tis_mask_zarr, tis_mask_meta, mask_name="Tissue")
    tissue_mask = tissue_mask_scematk.image
    footprint = disk(tissue_mask_scematk.pixel_from_micron(100))
    qc_mask = binary_erosion(tissue_mask, structure=footprint)
    qc_mask_labeled, _ = label(qc_mask)
    start_time = time()
    da.to_zarr(qc_mask_labeled, os.path.join(paths["mask_qc"], "mask_qc.zarr"))
    end_time = time()
    benchmarks["mask_qc"] = end_time - start_time
    logger.info("COMPLETED: Generating QC Mask")
