import argparse

from zipfify import ZipfReader
from lemmatize import LemmaZipfReader, LANGUAGES

parser = argparse.ArgumentParser(description="Convert pdfs into word-frequency lists.")

parser.add_argument("-f", "--filepath", help="Path to target pdf")

parser.add_argument(
    "-s",
    "--sections",
    help="Divide work frequency list by sections. Leave empty to calculate the global word frequency list. Must be either single number (the number of pages per section) or a sequence of starting indices of each section (i.e., \"0 10 20 30\"). ", nargs="+", default=0,
)

parser.add_argument(
    "-n",
    "--show-numbers",
    dest="numbers",
    help="Whether to show the count next to each entry (e.g., \"the 182\"\")",
    action="store_true"
)
parser.add_argument(
    "--hide-numbers",
    dest="numbers",
    help="Whether to show the count next to each entry (e.g., \"the 182\"\"). By default, numbers are hidden",
    action="store_false"
)
parser.set_defaults(numbers=False)

parser.add_argument(
    "-d",
    "--show-duplicates",
    dest="duplicates",
    help="To be used in conjuction with ``--sections``. Whether to show words if they have already occurred in an earlier section.",
    action="store_true",
)
parser.add_argument(
    "--hide-duplicates",
    dest="duplicates",
    help="To be used in conjuction with ``--sections``. Whether to show words if they have already occurred in an earlier section.By default, duplicates are hidden",
    action="store_false",
)
parser.set_defaults(duplicates=False)

parser.add_argument(
    "-l",
    "--language",
    help="To specify language. Leave blank for generic (non-lemmatized) handling.",
    choices=[None, *LANGUAGES],
    default=None
)

if __name__ == "__main__":
    args = parser.parse_args()

    filepath = args.filepath
    show_duplicates = args.duplicates
    show_numbers = args.numbers
    language = args.language

    zipf_reader = ZipfReader(filepath)

    if language:
        zipf_reader = LemmaZipfReader(filepath, language)

    if args.sections:
        sections = list(map(lambda s: int(s), args.sections)) # Convert to ints

        if len(sections) == 1:
            sections = sections[0]

        print(
            *zipf_reader.pretty_print_word_freqs_by_section(
                sections, show_numbers=show_numbers, show_duplicates=show_duplicates
            ),
            sep="\n"
        )

    else:
        print(zipf_reader.pretty_print_word_freqs(show_numbers))
