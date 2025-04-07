from argparse import Namespace
import dask.array as da
from dask_image.ndmeasure import label
from dask_image.ndmorph import binary_erosion
from logging import Logger
import os
from scematk.io import read_zarr_bin_mask
from shutil import rmtree
from skimage.morphology import disk
from time import time

def create_qc_mask(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Generating QC Mask")
    tis_mask_dir = paths["mask_tissue"]
    tis_mask_zarr = os.path.join(tis_mask_dir, "img.zarr")
    tis_mask_meta = os.path.join(tis_mask_dir, "meta.json")
    tissue_mask_scematk = read_zarr_bin_mask(tis_mask_zarr, tis_mask_meta, mask_name="Tissue")
    tissue_mask = tissue_mask_scematk.image
    downsampled_image = da.coarsen(da.mean, tissue_mask, {0:32, 1:32}) > 0.5
    footprint = disk(tissue_mask_scematk.pixel_from_micron(250/32))
    qc_mask = binary_erosion(downsampled_image, structure=footprint)
    qc_mask = qc_mask.rechunk((4096, 4096)) #TODO: Install fix
    temp_dir = os.path.join(paths["mask_qc"], "temp.zarr")
    da.to_zarr(qc_mask, temp_dir)
    qc_mask = da.from_zarr(temp_dir)
    qc_mask_labeled, _ = label(qc_mask)
    qc_mask_labeled = qc_mask_labeled.rechunk((4096, 4096))
    da.to_zarr(qc_mask_labeled, os.path.join(paths["mask_qc"], "mask_qc.zarr"))
    rmtree(temp_dir)
    logger.info("COMPLETED: Generating QC Mask")
