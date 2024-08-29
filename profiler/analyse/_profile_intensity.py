from argparse import Namespace
from logging import Logger
import os
from scematk.io import read_zarr_lbl_mask, read_zarr_ubimg
from scematk.morphology import MorphologicalProfiler
from time import time

def profile_intensity(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Profiling intensity morphology")
    deconv_dir = paths["img_deconv"]
    deconv_zarr = os.path.join(deconv_dir, "img.zarr")
    deconv_meta = os.path.join(deconv_dir, "meta.json")
    nuc_dir = paths["mask_nuc"]
    nuc_zarr = os.path.join(nuc_dir, "img.zarr")
    nuc_meta = os.path.join(nuc_dir, "meta.json")
    cell_dir = paths["mask_cell"]
    cell_zarr = os.path.join(cell_dir, "img.zarr")
    cell_meta = os.path.join(cell_dir, "meta.json")
    cyto_dir = paths["mask_cyto"]
    cyto_zarr = os.path.join(cyto_dir, "img.zarr")
    cyto_meta = os.path.join(cyto_dir, "meta.json")
    out_dir = os.path.join(paths["data_staged"], "intensity.csv")
    deconv_image = read_zarr_ubimg(deconv_zarr, deconv_meta, channel_names=["Hematoxylin", "DAB"])
    nuc_mask = read_zarr_lbl_mask(nuc_zarr, nuc_meta, mask_name="Nuclei")
    cell_mask = read_zarr_lbl_mask(cell_zarr, cell_meta, mask_name="Cell")
    cyto_mask = read_zarr_lbl_mask(cyto_zarr, cyto_meta, mask_name="Cytoplasm")
    mp = MorphologicalProfiler(["no-centroids", "intensity"], block_size=8192)
    data = mp.measure(deconv_image, [nuc_mask, cell_mask, cyto_mask])
    start_time = time()
    data.to_csv(out_dir, index=False, single_file=True)
    end_time = time()
    benchmarks["profile_intensity"] = end_time - start_time
    logger.info("COMPLETED: Profiled area and shape morphology")