from .utils._argument_parser import get_cli_args
from .utils._generate_paths import generate_paths
from .utils._logger import get_logger
from time import time

if __name__=='__main__':
    start_time = time()
    args = get_cli_args()
    logger = get_logger(args)
    paths = generate_paths(args, logger)
    metadata = {}
    benchmarks = {}
    