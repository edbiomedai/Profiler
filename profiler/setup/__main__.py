from .utils._argument_parser import get_cli_args
from .utils._populate_dirs import populate_dirs

def main() -> None:
    args = get_cli_args()
    populate_dirs()

if __name__ == "__main__":
    main()
