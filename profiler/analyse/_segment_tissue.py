from argparse import Namespace
from logging import Logger
import numpy as np
import os
from PIL import Image
from scematk.io import read_zarr_ubimg
from scematk.process import Processor
from scematk.process.colour import RGBToGrey
from scematk.process.contrast import GammaContrast
from scematk.process.morphology import BinaryClosing, BinaryOpening
from scematk.segment.tissue import OtsuThresholder
from time import time

def segment_tissue(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Segmenting tissue")
    norm_dir = paths["img_norm"]
    norm_zarr = os.path.join(norm_dir, "img.zarr")
    norm_meta = os.path.join(norm_dir, "meta.json")
    out_dir = paths["mask_tissue"]
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    raw_image = read_zarr_ubimg(norm_zarr, norm_meta)
    preproc = Processor([RGBToGrey(), GammaContrast(5)])
    postproc = Processor([BinaryClosing(2), BinaryOpening(2)])
    start_time = time()
    otsu_thresholder = OtsuThresholder(preprocessor = preproc, postprocessor = postproc)
    otsu_thresholder.fit(raw_image)
    end_time = time()
    benchmarks["fit_otsu"] = end_time - start_time
    start_time = time()
    tissue_mask = otsu_thresholder.run(raw_image)
    tissue_mask.save(out_zarr, out_meta)
    end_time = time()
    benchmarks["run_otsu"] = end_time - start_time
    logger.info("COMPLETED: Segmented tissue")
    logger.info("STARTED: Creating tissue mask thumbnail")
    thumb_out = os.path.join(paths["thumb_mask_tissue"], args.image + ".png")
    thumb = tissue_mask.get_thumb() * 255
    thumb = thumb.astype(np.uint8)
    thumb = Image.fromarray(thumb)
    thumb.save(thumb_out)
    logger.info("COMPLETED: Created tissue mask thumbnail")