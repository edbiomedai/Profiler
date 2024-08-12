from argparse import ArgumentParser, Namespace


def get_cli_args() -> Namespace:
    parser = ArgumentParser("Setup directory for analysis")
    parser.add_argument("--norm-target", type=str, help="Normalisation target", required=True)
    
    convert_parser = parser.add_argument_group("Convert TIFF to Zarr")
    convert_parser.add_argument(
        "--convert-tile-size", help="Tile size of conversion", type=int, default=4096
    )
    convert_parser.add_argument(
        "--convert-chunk-size", help="Chunk size of conversion", type=int, default=4096
    )
    return parser.parse_args()
