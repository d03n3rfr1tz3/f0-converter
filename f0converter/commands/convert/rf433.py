from ...errors import ConvertError
from ...inputs import InputSettings
from ...names import parse_rename
from ...outputs.rf433 import Rf433Options, Rf433Output
from ...signal.cluster import DEFAULT_TOLERANCE
from ...signal.frames import DEFAULT_MIN_GAP
from .base import ConvertCommand


class Rf433Command(ConvertCommand):
    name = "rf433"
    help = "SubGhz files (.sub) to rf433 codes"
    output_class = Rf433Output
    file_pattern = "Christmas/*.sub"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--remote", help="write a complete code file for this remote")
        parser.add_argument("--repeat", type=int, help="repeat of the remote, only with --remote")
        parser.add_argument("--name", help="code name, only for one file (default: file name)")
        parser.add_argument("--rename-suffix", action="append", default=[], type=parse_rename, metavar="OLD=NEW",
                            help="rename the end of code names, e.g. On=an turns Light_On into Light_an")
        parser.add_argument("--min-gap", type=int, default=DEFAULT_MIN_GAP,
                            help="pauses of at least this many µs end a recorded frame (default %(default)s)")
        parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE,
                            help="relative distance of values that count as equal (default %(default)s)")

    def check_paths(self, paths, args):
        if args.name is not None and len(paths) != 1:
            raise ConvertError("--name needs exactly one file, got %d" % len(paths))
        if args.repeat is not None and args.remote is None:
            raise ConvertError("--repeat needs --remote")

    def input_settings(self, args):
        return InputSettings(args.min_gap, args.tolerance)

    def output_options(self, args, extensions):
        return Rf433Options(extensions, remote=args.remote, repeat=args.repeat, name=args.name,
                            renames=args.rename_suffix, tolerance=args.tolerance)
