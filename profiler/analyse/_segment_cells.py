from argparse import Namespace
from logging import Logger
import os
from scematk.io import read_zarr_lbl_mask
from scematk.segment.secondary import ExpansionSegmenter
from time import time

def segment_cells(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Segmenting cells")
    nuc_dir = paths["mask_nuc"]
    nuc_zarr = os.path.join(nuc_dir, "img.zarr")
    nuc_meta = os.path.join(nuc_dir, "meta.json")
    out_dir = paths["mask_cell"]
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    nuclei_mask = read_zarr_lbl_mask(nuc_zarr, nuc_meta, mask_name="Nuclei")
    expansion_segmenter = ExpansionSegmenter(5)
    cell_mask = expansion_segmenter.run(nuclei_mask)
    cell_mask.set_channel_names("Cell")
    start_time = time()
    cell_mask.save(out_zarr, out_meta)
    end_time = time()
    benchmarks["segment_cells"] = end_time - start_time
    logger.info("COMPLETED: Segmented cells")