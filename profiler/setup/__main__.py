from .analyse._convert_norm_target import prep_norm_target
from .utils._argument_parser import get_cli_args
from .utils._populate_dirs import populate_dirs

def main() -> None:
    args = get_cli_args()
    populate_dirs()
    prep_norm_target(args)

if __name__ == "__main__":
    main()
