from .analyse._apply_qc import apply_qc
from .analyse._convert_tiff_to_zarr import convert_tiff_to_zarr
from .analyse._create_qc_mask import create_qc_mask
from .analyse._deconvolve_image import deconvolve_image
from .analyse._extract_image_metadata import extract_image_metadata
from .analyse._segment_nuclei import segment_nuclei
from .analyse._extract_tissue_metadata import extract_tissue_metadata
from .analyse._merge_data import merge_data
from .analyse._profile_areashape import profile_areashape
from .analyse._profile_intensity import profile_intensity
from .analyse._segment_cells import segment_cells
from .analyse._segment_cytoplasms import segment_cytoplasms
from .analyse._segment_tissue import segment_tissue
from .analyse._normalise_image import normalise_image
from .analyse._process_nuc_mask import process_nuc_mask
from .utils._argument_parser import get_cli_args
from .utils._generate_paths import generate_paths
from .utils._logger import get_logger
import json
import os
import pandas as pd
from shutil import rmtree
from time import time


def main() -> None:
    start_time = time()
    args = get_cli_args()
    logger = get_logger(args)
    paths = generate_paths(args, logger)
    metadata = {}
    benchmarks = {}
    benchmarks["image_name"] = os.path.basename(args.image)
    convert_tiff_to_zarr(args, logger, paths, benchmarks)
    extract_image_metadata(args, logger, paths, metadata)
    normalise_image(args, logger, paths, benchmarks)
    rmtree(paths["img_raw"])
    deconvolve_image(args, logger, paths, benchmarks)
    segment_tissue(args, logger, paths, benchmarks)
    extract_tissue_metadata(args, logger, paths, metadata)
    segment_nuclei(args, logger, paths, benchmarks)
    rmtree(paths["img_norm"])
    process_nuc_mask(args, logger, paths, benchmarks)
    rmtree(paths["mask_nuc_unproc"])
    segment_cells(args, logger, paths, benchmarks)
    segment_cytoplasms(args, logger, paths, benchmarks)
    profile_areashape(args, logger, paths, benchmarks)
    profile_intensity(args, logger, paths, benchmarks)
    rmtree(paths["img_deconv"])
    rmtree(paths["mask_cell"])
    rmtree(paths["mask_cyto"])
    rmtree(paths["mask_nuc"])
    create_qc_mask(args, logger, paths, benchmarks)
    rmtree(paths["mask_tissue"])
    apply_qc(args, logger, paths, benchmarks)
    rmtree(paths["mask_qc"])
    
    merge_data(args, logger, paths, benchmarks)
    rmtree(paths["data_staged"])
    
    logger.info("STARTED: Export Metadata")
    end_time = time()
    elapsed_time = end_time - start_time
    benchmarks["whole_workflow"] = elapsed_time
    benchmarks_out_dir = os.path.join(paths["benchmarks"], os.path.basename(args.image) + ".csv")
    pd.DataFrame(benchmarks, index=[0]).to_csv(benchmarks_out_dir, index=False)
    metadata_out_dir = os.path.join(paths["metadata"], os.path.basename(args.image) + ".csv")
    pd.DataFrame(metadata, index=[0]).to_csv(metadata_out_dir, index=False)
    logger.info("COMPLETED: Export Metadata")

if __name__ == "__main__":
    main()
