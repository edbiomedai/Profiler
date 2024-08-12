from argparse import Namespace
from logging import Logger
from PIL import Image
from scematk.io import read_zarr_ubimg, tiff_to_zarr
from time import time
import os


def convert_tiff_to_zarr(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Converting TIFF to zarr")
    img_dir = paths["img"]
    out_dir = paths["img_raw"]
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    start_time = time()
    try:
        tiff_to_zarr(
            img_dir,
            out_zarr,
            out_meta,
            tile_size=args.convert_tile_size,
            chunk_size=args.convert_chunk_size,
        )
    except Exception as e:
        logger.error(f"ERROR: Image could not be converted to zarr with error:\n{e}")
        raise RuntimeError()
    logger.info("COMPLETED: Converted TIFF to zarr")
    end_time = time()
    elapsed_time = end_time - start_time
    benchmarks["convert_tiff"] = elapsed_time
    logger.info("STARTED: Creating raw image thumbnail")
    thumb_out = os.path.join(paths["thumb_raw"], args.image + ".png")
    image = read_zarr_ubimg(out_zarr, out_meta)
    image = image.get_thumb()
    image = Image.fromarray(image)
    image.save(thumb_out)
    logger.info("COMPLETED: Created raw image thumbnail")
