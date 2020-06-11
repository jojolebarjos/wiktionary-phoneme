
import io

from tqdm import tqdm

from . import (
    iterate_dump,
    tqdm_file,
)


def extract(parse, input_file, output_file):

    # Make sure we got a file object as input
    if isinstance(input_file, str):
        input_file = io.open(input_file, "rb")

    # Get compressed dump size in bytes
    size = input_file.seek(0, io.SEEK_END)
    input_file.seek(0)

    # Wrap with progress bar
    with tqdm_file(input_file, total=size, unit="B", unit_scale=True, unit_divisor=1024) as input_file:

        # Make sure we got a file object as output
        if isinstance(output_file, str):
            output_file = io.open(output_file, "w", encoding="utf-8", newline="\n")

        # Do the thing
        with output_file:
            for title, content in iterate_dump(input_file):
                for text, language, pronunciation in parse(title, content):
                    output_file.write(f"{text}\t{language}\t{pronunciation}\n")
