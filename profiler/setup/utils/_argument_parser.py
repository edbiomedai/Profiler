from argparse import ArgumentParser, Namespace


def get_cli_args() -> Namespace:
    parser = ArgumentParser("Setup directory for analysis")
    parser.add_argument("--norm-target", type=str, help="Normalisation target", required=True)
    return parser.parse_args()
