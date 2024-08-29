from argparse import Namespace
from logging import Logger
import os
from scematk.io import read_zarr_bin_mask, read_zarr_lbl_mask
from scematk.segment import clip_mask

def process_nuc_mask(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Processing nuclei")
    mask_dir = paths["mask_nuc_unproc"]
    mask_zarr = os.path.join(mask_dir, "img.zarr")
    mask_meta = os.path.join(mask_dir, "meta.json")
    out_dir = paths["mask_nuc"]
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    unproc_mask = read_zarr_lbl_mask(mask_zarr, mask_meta, mask_name="Nuclei")
    tis_dir = paths["mask_tissue"]
    tis_zarr = os.path.join(tis_dir, "img.zarr")
    tis_meta = os.path.join(tis_dir, "meta.json")
    tissue_mask = read_zarr_bin_mask(tis_zarr, tis_meta)
    proc_mask = clip_mask(unproc_mask, tissue_mask)
    proc_mask.save(out_zarr, out_meta)
    logger.info("COMPLETED: Processed nuclei")