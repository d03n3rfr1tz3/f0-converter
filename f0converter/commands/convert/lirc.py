from ...errors import ConvertError
from ...outputs.lirc import LircOptions, LircOutput
from .base import ConvertCommand


class LircCommand(ConvertCommand):
    name = "lirc"
    help = "IR files (.ir) to LIRC remote files"
    output_class = LircOutput
    file_pattern = "infrared/*.ir"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("--remote", help="name of the remote, only for one file (default: file name)")
        parser.add_argument("--output", help="folder for <file name>.lircd.conf, needed for several files (default: stdout)")

    def check_paths(self, paths, args):
        if args.remote is not None and len(paths) != 1:
            raise ConvertError("--remote needs exactly one file, got %d" % len(paths))
        if args.output is None and len(paths) != 1:
            raise ConvertError("%d files need --output" % len(paths))

    def output_options(self, args, extensions):
        return LircOptions(extensions, remote=args.remote)
