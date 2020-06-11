
import argparse
import io

import regex as re

from . import (
    get_parser,
    iterate_dump,
)


def process(parse, input_file, output_file):

    if isinstance(output_file, str):
        output_file = io.open(output_file, "w", encoding="utf-8", newline="\n")

    try:
        for title, content in iterate_dump(input_file):
            for text, language, pronunciation in parse(title, content):
                output_file.write(f"{text}\t{language}\t{pronunciation}\n")

    finally:
        output_file.close()


parser = argparse.ArgumentParser(description="Extract IPA from Wiktionary dump")
parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("--language", "-l", nargs="?", help="Wikipedia language code")

args = parser.parse_args()

if args.language is None:
    match = re.match(r'^(\w+)wiktionary', args.input)
    if not match:
        raise ValueError('Failed to infer language')
    args.language = match.group(1)

parse = get_parser(args.language)

process(parse, args.input, args.output)
