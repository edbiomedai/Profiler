from argparse import Namespace
from logging import Logger
import os

def generate_paths(args: Namespace, logger: Logger) -> dict:
    logger.info("STARTED: Creating image paths")
    cwd = os.getcwd()
    paths = {
        "img_raw": os.path.join(cwd, "imgs", "raw", args.image),
        "img_norm": os.path.join(cwd, "imgs", "norm", args.image),
        "img_deconv": os.path.join(cwd, "imgs", "deconv", args.image),
        "mask_tissue": os.path.join(cwd, "imgs", "mask_tissue", args.image),
        "mask_nuc_unproc": os.path.join(cwd, "imgs", "mask_nuc_unproc", args.image),
        "mask_nuc": os.path.join(cwd, "imgs", "mask_nuc", args.image),
        "mask_cell": os.path.join(cwd, "imgs", "mask_cell", args.image),
        "mask_cyto": os.path.join(cwd, "imgs", "mask_cyto", args.image),
        "data": os.path.join(cwd, "data", args.image),
        "data_staged": os.path.join(cwd, "data", "staged", args.image)
    }
    for path in paths.values():
        os.mkdir(path)
    paths["img"] = os.path.join(cwd, args.image)
    paths["norm_target"] = os.path.join(cwd, "norm_target")
    paths["thumb_raw"] = os.path.join(cwd, "thumbs", "raw")
    paths["thumb_norm"] = os.path.join(cwd, "thumbs", "norm")
    paths["thumb_deconv"] = os.path.join(cwd, "thumbs", "deconv")
    paths["thumb_mask_tissue"] = os.path.join(cwd, "thumbs", "mask_tissue")
    paths["metadata"] = os.path.join(cwd, "metadata")
    paths["benchmarks"] = os.path.join(cwd, "benchmarks")
    logger.info("COMPLETED: Created image paths")
    return paths