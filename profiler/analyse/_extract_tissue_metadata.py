from argparse import Namespace
from logging import Logger
import os
from scematk.io import read_zarr_bin_mask

def extract_tissue_metadata(args: Namespace, logger: Logger, paths: dict, metadata: dict) -> None:
    tis_dir = paths["mask_tissue"]
    tis_zarr = os.path.join(tis_dir, "img.zarr")
    tis_meta = os.path.join(tis_dir, "meta.json")
    tissue_mask = read_zarr_bin_mask(tis_zarr, tis_meta)
    metadata["tissue_area"] = tissue_mask.image.sum().compute()
    logger.info("STATUS: Extracted tissue mask metadata")