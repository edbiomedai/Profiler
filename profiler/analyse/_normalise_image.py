from argparse import Namespace
from logging import Logger
import os
from PIL import Image
from scematk.io import read_zarr_ubimg
from scematk.normalise import ReinhardNormaliser
from time import time

def normalise_image(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Normalising image")
    cwd = os.getcwd()
    raw_dir = os.path.join(cwd, "imgs", "raw", args.image)
    raw_zarr = os.path.join(raw_dir, "img.zarr")
    raw_meta = os.path.join(raw_dir, "meta.json")
    out_dir = os.path.join(cwd, "imgs", "norm", args.image)
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    norm_target_dir = os.path.join(cwd, "norm_target")
    norm_target_zarr = os.path.join(norm_target_dir, "img.zarr")
    norm_target_meta = os.path.join(norm_target_dir, "meta.json")
    raw_image = read_zarr_ubimg(raw_zarr, raw_meta)
    norm_target = read_zarr_ubimg(norm_target_zarr, norm_target_meta)
    normaliser = ReinhardNormaliser()
    start_time = time()
    normaliser.fit(norm_target)
    end_time = time()
    benchmarks["fit_norm"] = end_time - start_time
    start_time = time()
    norm_image = normaliser.run(raw_image)
    norm_image.save(out_zarr, out_meta)
    end_time = time()
    benchmarks["run_norm"] = end_time - start_time
    logger.info("COMPLETED: Normalised image")
    logger.info("STARTED: Creating normalised thumbnail")
    norm_image = read_zarr_ubimg(out_zarr, out_meta)
    thumb = norm_image.get_thumb()
    thumb = Image.fromarray(thumb)
    out_path = os.path.join(paths["thumb_norm"], args.image + ".png")
    thumb.save(out_path)
    logger.info("COMPLETED: Created normalised image thumbnail")