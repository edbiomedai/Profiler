from argparse import Namespace
import dask.array as da
from logging import Logger
import numpy as np
import os
from PIL import Image
from scematk.image import BinaryMask
from scematk.image._image import Image as SCEMATKImage
from scematk.io import read_zarr_ubimg
from scematk.process import Processor
from scematk.process._process import Process
from scematk.process.colour import RGBToGrey
from scematk.process.contrast import GammaContrast
from scematk.process.morphology import BinaryClosing, BinaryOpening
from scematk.segment.tissue import OtsuThresholder
from time import time

class Downsample(Process):
    def __init__(self):
        super().__init__("downsampler")
    
    def run(self, image: SCEMATKImage) -> SCEMATKImage:
        img = image.image
        downsampled_image = da.coarsen(da.mean, img, {0:32, 1:32}) > 0.5
        return BinaryMask(downsampled_image.rechunk((4096, 4096)), image.info, ["Tissue"])
    
class Upsample(Process):
    def __init__(self):
        super().__init__("upsampler")
    
    def run(self, image: SCEMATKImage) -> SCEMATKImage:
        img = image.image
        upsampled_image_intermediate = da.repeat(img, 32, axis=0)
        upsampled_image = da.repeat(upsampled_image_intermediate, 32, axis=1)
        return BinaryMask(upsampled_image.rechunk((4096, 4096)), image.info, ["Tissue"])

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
    postproc = Processor([Downsample(), BinaryClosing(3), BinaryOpening(8), Upsample()])
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