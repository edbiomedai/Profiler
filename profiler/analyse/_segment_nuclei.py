from argparse import Namespace
from csbdeep.data import Normalizer, normalize_mi_ma
from logging import Logger
import numpy as np
import os
from shutil import copy
from stardist.models import StarDist2D
from time import time
import zarr

def segment_nuclei(args: Namespace, logger: Logger, paths: dict, benchmarks: dict) -> None:
    logger.info("STARTED: Segmenting nuclei")
    norm_dir = paths["img_norm"]
    norm_zarr = os.path.join(norm_dir, "img.zarr")
    norm_meta = os.path.join(norm_dir, "meta.json")
    out_dir = paths["mask_nuc_unproc"]
    out_zarr = os.path.join(out_dir, "img.zarr")
    in_zarr = zarr.open(norm_zarr)
    store = zarr.DirectoryStore(out_zarr)
    out_zarr = zarr.create(shape=in_zarr.shape[:2], chunks=(4096, 4096), dtype=np.int32, store=store)
    class MyNormalizer(Normalizer):
        def __init__(self, mi, ma):
            self.mi, self.ma = mi, ma

        def before(self, x, axes):
            return normalize_mi_ma(x, self.mi, self.ma, dtype=np.float32)

        def after(*args, **kwargs):
            assert False

        @property
        def do_after(self):
            return False

    mi, ma = 0, 255
    normalizer = MyNormalizer(mi, ma)
    sd_model = StarDist2D.from_pretrained("2D_versatile_he")
    start_time = time()
    _, _ = sd_model.predict_instances_big(
        in_zarr,
        axes="YXC",
        block_size=4096,
        min_overlap=128,
        context=128,
        normalizer=normalizer,
        n_tiles=(4,4,1),
        labels_out=out_zarr,
        prob_thresh=0.2,
        nms_thresh=0.3,
    )
    end_time = time()
    benchmarks["segment_nuclei"] = end_time - start_time
    copy(norm_meta, out_dir)
    logger.info("COMPLETED: Segmented nuclei")