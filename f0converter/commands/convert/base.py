"""The common flow of all conversions: paths -> input -> output -> stdout or files."""

from __future__ import annotations

import argparse
import glob
import os

from ...errors import ConvertError
from ...extensions import EXTENSIONS, Extension, find_extension
from ...inputs import INPUTS, InputSettings, read_input
from ...messages import Messages
from ...outputs import Document, Output, OutputOptions
from ..base import Command


def expand_paths(patterns: list[str]) -> list[str]:
    """Patterns are expanded here, so they work on Windows as well."""
    paths = []
    for pattern in patterns:
        matches = sorted(glob.glob(pattern)) if glob.has_magic(pattern) else [pattern]
        if not matches:
            raise ConvertError("no files match " + pattern)
        paths.extend(matches)
    return paths


class ConvertCommand(Command):
    output_class: type[Output] = Output
    file_pattern = "remotes/*"          # example in the help text

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("files", nargs="+", help="files or patterns like %s" % self.file_pattern)
        parser.add_argument("--from", dest="input", choices=[item.name for item in INPUTS],
                            help="input format (default: recognized by the content)")
        parser.add_argument("--extension", action="append", default=[], choices=[item.name for item in EXTENSIONS],
                            help="add comments for other tools, see docs/extensions.md")

    def check_paths(self, paths: list[str], args: argparse.Namespace) -> None:
        pass

    def input_settings(self, args: argparse.Namespace) -> InputSettings:
        return InputSettings()

    def output_options(self, args: argparse.Namespace, extensions: list[Extension]) -> OutputOptions:
        return OutputOptions(extensions)

    def run(self, args: argparse.Namespace, messages: Messages) -> int:
        paths = expand_paths(args.files)
        self.check_paths(paths, args)
        extensions = [find_extension(name) for name in args.extension]
        settings = self.input_settings(args)

        results = []
        for path in paths:
            where = os.path.basename(path)
            try:
                result = read_input(path, settings, args.input)
            except (ConvertError, OSError) as error:
                messages.error(where, str(error))
                continue
            for warning in result.warnings:
                messages.warning(where, warning)
            for error in result.errors:
                messages.error(where, error)
            results.append(result)

        documents = self.output_class().convert(results, self.output_options(args, extensions), messages) if results else []
        self.emit(documents, getattr(args, "output", None), messages)
        return 1 if messages.errors else 0

    def emit(self, documents: list[Document], folder: str | None, messages: Messages) -> None:
        for document in documents:
            if folder is None:
                print(document.text, end="")
                continue
            target = os.path.join(folder, document.name)
            if os.path.exists(target):
                messages.error(target, "exists, delete it first or choose another --output")
                continue
            os.makedirs(folder, exist_ok=True)
            with open(target, "w", encoding="utf-8", newline="\n") as file:
                file.write(document.text)
            messages.info("written " + target)
