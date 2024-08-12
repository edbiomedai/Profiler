from argparse import ArgumentParser, Namespace

def get_cli_args() -> Namespace:
    parser = ArgumentParser(description="Morphologically profile a WSI")
    parser.add_argument('--image', help='path to TIFF to analyse', type=str, required=True)
    
    convert_parser = parser.add_argument_group("Convert TIFF to Zarr")
    convert_parser.add_argument("--convert-tile-size", help='Tile size of conversion', type=int, default=4096)
    convert_parser.add_argument("--convert-chunk-size", help='Chunk size of conversion', type=int, default=4096)
    return parser.parse_args()