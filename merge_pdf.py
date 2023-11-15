from __future__ import annotations

import os
import shutil
import tempfile
from argparse import ArgumentParser
from logging import getLogger
from pathlib import Path
from collections.abc import Sequence

from PyPDF2 import PdfMerger

logger = getLogger(__name__)


def get_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument("files", nargs="*", help="PDF files to merge")
    parser.add_argument(
        "-a", "--all", help="merge all pdfs in the directory, and save as *all*"
    )
    return parser


def discover_all() -> list[str]:
    files = []
    for file in os.listdir():
        if file.endswith(".pdf"):
            files.append(file)
    return files


def merge(files: Sequence[str], out: str) -> None:
    with tempfile.TemporaryDirectory(suffix="merge-pdf") as tmpdir:
        t_file = Path(tmpdir) / "out.pdf"
        with PdfMerger() as merger:
            for file in files:
                merger.append(file)
            merger.write(str(t_file))

        shutil.copy(str(t_file), out)


def main() -> int:
    parser = get_parser()
    args = parser.parse_args()
    if not args.files:
        if args.all is not None:
            logger.warning(
                f"merging all pdfs in the directory and saving as {args.all}"
            )
            merge(discover_all(), args.all)
            return 0
        else:
            logger.error("no files to merge")
            return 1
    elif len(args.files) < 3:
        logger.error("at least 3 files are required")
        return 1
    else:
        logger.warning(
            f"merging {args.files[:-1]} pdfs in "
            f"the directory and saving as {args.files[-1]}"
        )
        merge(args.files[:-1], args.files[-1])
        return 0
