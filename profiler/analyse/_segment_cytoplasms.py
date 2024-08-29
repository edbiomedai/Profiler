from argparse import Namespace
from logging import Logger
import os
from scematk.io import read_zarr_lbl_mask
from scematk.segment.tertiary import subtract_mask
from time import time

def segment_cytoplasms(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Segmenting cyoplasms")
    nuc_dir = paths["mask_nuc"]
    nuc_zarr = os.path.join(nuc_dir, "img.zarr")
    nuc_meta = os.path.join(nuc_dir, "meta.json")
    cell_dir = paths["mask_cell"]
    cell_zarr = os.path.join(cell_dir, "img.zarr")
    cell_meta = os.path.join(cell_dir, "meta.json")
    out_dir = paths["mask_cyto"]
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    nuclei_mask = read_zarr_lbl_mask(nuc_zarr, nuc_meta, mask_name="Nuclei")
    cell_mask = read_zarr_lbl_mask(cell_zarr, cell_meta, mask_name="Cell")
    cyto_mask = subtract_mask(cell_mask, nuclei_mask, mask_name="Cytoplasm")
    start_time = time()
    cyto_mask.save(out_zarr, out_meta)
    end_time = time()
    benchmarks["segment_cyto"] = end_time - start_time
    logger.info("COMPLETED: Segmented cytoplasms")