import argparse
import io

import regex as re

from tqdm import tqdm

from . import (
    get_cleaner,
    get_parser,
    extract,
)


parser = argparse.ArgumentParser(description="Extract IPA from Wiktionary dump")
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--language", "-l", nargs="?", help="Wikipedia language code")
parser.add_argument("--raw", "-r", action="store_true", help="Disable cleaning step")

args = parser.parse_args()

# Try to infer language from name
if args.language is None:
    match = re.match(r"^(\w+)wiktionary", args.input)
    if not match:
        raise ValueError("Failed to infer language")
    args.language = match.group(1)

parse = get_parser(args.language)

if args.raw:
    clean = None
else:
    clean = get_cleaner(args.language)

extract(args.input, args.output, parse, clean)
