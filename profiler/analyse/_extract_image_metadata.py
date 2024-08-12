from argparse import Namespace
from logging import Logger
import numpy as np
import os
from scematk.io import read_zarr_ubimg

def extract_image_metadata(args: Namespace, logger: Logger, paths: dict, metadata: dict) -> None:
    raw_dir = paths["img_raw"]
    raw_zarr = os.path.join(raw_dir, "img.zarr")
    raw_meta = os.path.join(raw_dir, "meta.json")
    raw_image = read_zarr_ubimg(raw_zarr, raw_meta)
    metadata["image_name"] = os.path.basename(args.image)
    metadata['format'] = raw_image.info['format']
    metadata["ydim"] = raw_image.shape[0]
    metadata["xdim"] = raw_image.shape[1]
    metadata["area"] = np.prod(raw_image.shape[:2])
    metadata["mpp"] = raw_image.mpp
    logger.info("STATUS: Extracted image metadata")