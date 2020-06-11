
import argparse
import io

import regex as re

from tqdm import tqdm

from . import (
    get_parser,
    extract,
)


parser = argparse.ArgumentParser(description="Extract IPA from Wiktionary dump")
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--language", "-l", nargs="?", help="Wikipedia language code")

args = parser.parse_args()

# Try to infer language from name
if args.language is None:
    match = re.match(r'^(\w+)wiktionary', args.input)
    if not match:
        raise ValueError('Failed to infer language')
    args.language = match.group(1)

parse = get_parser(args.language)

extract(parse, args.input, args.output)
