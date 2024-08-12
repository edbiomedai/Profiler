from argparse import Namespace
import logging
from logging import Logger
import os


def get_logger(args: Namespace) -> Logger:
    cwd = os.getcwd()
    logging_dir = os.path.join(cwd, "logs")
    log_file = os.path.join(logging_dir, args.image + ".log")
    logger = logging.getLogger("Morphological Profiling")
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info("STATUS: Logger initialised")
    return logger
