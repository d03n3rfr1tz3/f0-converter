from __future__ import annotations

import argparse

from ..messages import Messages


class Command:
    """One subcommand of the command line."""

    name = ""
    help = ""

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        pass

    def run(self, args: argparse.Namespace, messages: Messages) -> int:
        raise NotImplementedError
