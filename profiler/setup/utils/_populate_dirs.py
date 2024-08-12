import os

POPULATE_DIRS = [
    "logs",
    "sumbmission_logs",
    "data",
    os.path.join("data", "staged"),
    "metadata",
    os.path.join("metadata", "staged"),
    "benchmarks",
    os.path.join("benchmarks", "staged"),
    "thumbs",
    os.path.join("thumbs", "raw"),
    os.path.join("thumbs", "norm"),
    os.path.join("thumbs", "deconv"),
    os.path.join("thumbs", "mask_tissue"),
    "imgs",
    os.path.join("imgs", "raw"),
    os.path.join("imgs", "norm"),
    os.path.join("imgs", "deconv"),
    os.path.join("imgs", "mask_tissue"),
    os.path.join("imgs", "mask_nuc_unproc"),
    os.path.join("imgs", "mask_nuc"),
    os.path.join("imgs", "mask_cell"),
    os.path.join("imgs", "mask_cyto"),
    'norm_target'
]   

def populate_dirs() -> None:
    cwd = os.getcwd()
    dirs = [os.path.join(cwd, path) for path in POPULATE_DIRS]
    for path in dirs:
        assert not os.path.exists(path), f"Directory {path} already exists, please remove and try again"
    for path in dirs:
        os.mkdir(path)