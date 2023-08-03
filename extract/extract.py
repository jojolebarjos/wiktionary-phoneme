import io

from tqdm import tqdm

from . import (
    iterate_dump,
    tqdm_file,
)


def extract(input_file, output_file, parse, clean=None):

    # Make sure we got a file object as input
    if isinstance(input_file, str):
        input_file = io.open(input_file, "rb")

    # Get compressed dump size in bytes
    size = input_file.seek(0, io.SEEK_END)
    input_file.seek(0)

    # Wrap with progress bar
    with tqdm_file(
        input_file,
        total=size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as input_file:

        # Make sure we got a file object as output
        if isinstance(output_file, str):
            output_file = io.open(output_file, "w", encoding="utf-8", newline="\n")

        # Do the thing
        with output_file:
            output_file.write("text\tlanguage\ttag\tpronunciation\n")
            for title, content in iterate_dump(input_file):
                for text, language, tag, pronunciation in parse(title, content):

                    # Apply cleaning, if any
                    if clean is not None:
                        result = clean(text, language, tag, pronunciation)
                        if result is None:
                            continue
                        text, language, tag, pronunciation = result

                    # Write entry
                    output_file.write(f"{text}\t{language}\t{tag}\t{pronunciation}\n")
