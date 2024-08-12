from .analyse._convert_tiff_to_zarr import convert_tiff_to_zarr
from .analyse._extract_image_metadata import extract_image_metadata
from .utils._argument_parser import get_cli_args
from .utils._generate_paths import generate_paths
from .utils._logger import get_logger
from time import time


def main() -> None:
    start_time = time()
    args = get_cli_args()
    logger = get_logger(args)
    paths = generate_paths(args, logger)
    metadata = {}
    benchmarks = {}
    convert_tiff_to_zarr(args, logger, paths, benchmarks)
    extract_image_metadata(args, logger, paths, metadata)


if __name__ == "__main__":
    main()
