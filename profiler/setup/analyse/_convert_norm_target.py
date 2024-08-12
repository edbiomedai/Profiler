from argparse import Namespace
import os
from scematk.io import tiff_to_zarr

def prep_norm_target(args: Namespace) -> None:
    cwd = os.getcwd()
    out_dir = os.path.join(cwd, "norm_target")
    out_zarr = os.path.join(out_dir, "img.zarr")
    out_meta = os.path.join(out_dir, "meta.json")
    tiff_to_zarr(args.norm_target, out_zarr, out_meta)
    try:
        tiff_to_zarr(
            args.norm_target,
            out_zarr,
            out_meta,
            tile_size=args.convert_tile_size,
            chunk_size=args.convert_chunk_size,
        )
    except Exception as e:
        raise RuntimeError()