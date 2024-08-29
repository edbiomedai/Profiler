from argparse import Namespace
from logging import Logger
import os
from PIL import Image
from scematk.deconvolve import NativeSKImageStainDeconvolver
from scematk.io import read_zarr_ubimg
from scematk.process import Processor
from scematk.process.contrast import LinearContrast
from time import time

def deconvolve_image(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Deconvolving image")
    norm_dir = paths["img_norm"]
    norm_zarr = os.path.join(norm_dir, "img.zarr")
    norm_meta = os.path.join(norm_dir, "meta.json")
    out_dir = paths["img_deconv"]
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    raw_image = read_zarr_ubimg(norm_zarr, norm_meta)
    nskid = NativeSKImageStainDeconvolver(stain_type='H&E')
    start_time = time()
    deconv_image = nskid.run(raw_image)
    deconv_image.save(out_zarr, out_meta)
    end_time = time()
    elapsed_time = end_time - start_time
    benchmarks["deconv_img"] = elapsed_time
    logger.info("Completed: Deconvolved image")
    logger.info("STARTED: Creating deconvolved thumbnail")
    proc = Processor([LinearContrast(5)])
    thumb = proc.run(deconv_image)
    thumb = thumb.get_thumb()
    thumb = Image.fromarray(thumb)
    thumb_path = os.path.join(paths["thumb_deconv"], args.image + ".png")
    thumb.save(thumb_path)
    logger.info("COMPLETED: Created deconvolved thumbnail")