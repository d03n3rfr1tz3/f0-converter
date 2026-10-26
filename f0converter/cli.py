from __future__ import annotations

import argparse
import sys
from typing import Sequence

from . import __version__
from .commands import COMMANDS
from .errors import ConvertError
from .messages import Messages


def build_parser(commands) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="f0-converter",
                                     description="Flipper Zero files to rf433 code files and LIRC remote files")
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    subparsers = parser.add_subparsers(dest="command", metavar="command", required=True)
    for command in commands:
        subparser = subparsers.add_parser(command.name, help=command.help, description=command.help)
        command.add_arguments(subparser)
        subparser.set_defaults(handler=command)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser([command() for command in COMMANDS]).parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        return args.handler.run(args, Messages()) or 0
    except (ConvertError, OSError) as error:
        sys.stdout.flush()
        print("Error: %s" % error, file=sys.stderr)
        return 1
