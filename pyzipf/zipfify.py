import sys, os
from typing import Union, List, Tuple
from collections import Counter

from PyPDF2 import PdfFileReader

PUNCTUATIONS = """!()[]{};:\"\,<>\./?@#$%^&;*_~™»"""
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"

class ZipfReader:
    def __init__(self, filepath: Union[str, "os.PathLike[Any]"]):
        self.filepath = filepath
        self.pdf_reader = PdfFileReader(filepath)

    @property
    def num_pages(self):
        return self.pdf_reader.numPages

    def page_to_word_list(self, page_index: int=0) -> List[str]:
        page = self.pdf_reader.getPage(page_index)

        raw_text = page.extractText()

        # First we replace line breaks with spaces and get rid of empty lines.

        dense_text = raw_text.replace("\n", "")

        # 1. ``extractText`` often omits spaces at line breaks.
        #    - Wherever we see a digit, we skip.
        #    - Wherever we see an uppercase directly following a lowercase, we insert a space.
        #    - Wherever we see a hyphen denoting continuing (e.g. "some\n-thing"), we rejoin.
        # 2. We also remove all punctuation and numbers (replacing this with spaces)
        # TODO: remove urls

        cleaned_text = ""

        for i in range(len(dense_text) - 1):
            if dense_text[i].isdigit():
                continue
            elif dense_text[i] in PUNCTUATIONS:
                cleaned_text += ' '
            elif dense_text[i] == '-' and dense_text[i + 1].isalpha():
                continue
            elif not dense_text[i].isupper() and dense_text[i + 1].isupper():
                cleaned_text += dense_text[i] + ' '
            else:
                cleaned_text += dense_text[i]

        raw_list = cleaned_text.split(" ")

        # Get rid of nonce words (i.e., empty strings and consonants)
        # TODO: Include minimum word length
        cleaned_list = list(filter(lambda word: len(word) > 0 and word not in CONSONANTS, raw_list))

        return cleaned_list


    def page_range_to_word_freqs(self, initial_page: int, final_page: int) -> Counter:
        word_counter = Counter()

        # If ``final_page`` is greater than the number of pages in the document, we take the document length instead.
        for page_index in range(min(self.num_pages, final_page)):
            word_list = self.page_to_word_list(page_index)

            for word in word_list:
                word_counter[word] += 1

        return word_counter


    def get_word_freqs(self) -> Counter:
        return self.page_range_to_word_freqs(0, self.num_pages)

    def get_word_freqs_by_section(self, sections: Union[int, List[int]]) -> List[Counter]:
        """
        ``sections`` is either:
        1. An int for the number of pages per section, or
        2. A list of the indicies of the first page of every section.
        """
        word_freq_lists = []

        if type(sections) == int:
            for i in range(self.num_pages // sections + 1):
                word_freq_lists.append(self.page_range_to_word_freqs(i * sections, (i + 1) * sections))


        elif type(sections) == list:
            for i in range(len(sections) -1 ):
                word_freq_lists.append(self.page_range_to_word_freqs(sections[i], sections[i + 1]))
        else:
            raise ValueError("``sections`` must be either ``int`` or ``list``")

        return word_freq_lists


    def _pretty_print_freq_list(self, word_freqs: Counter, show_numbers: bool=True) -> str:
        word_freq_tuples = word_freqs.items()

        if show_numbers:
            return "".join(list(map(lambda wordfreq: f"{wordfreq[0].strip()} {wordfreq[1]}\n", word_freq_tuples)))

        return "".join(list(map(lambda wordfreq: f"{wordfreq[0].strip()}\n", word_freq_tuples)))


    def pretty_print_word_freqs(self, show_numbers: bool=True) -> str:
        word_freqs = self.get_word_freqs()

        return self._pretty_print_freq_list(word_freqs, show_numbers)

    def pretty_print_word_freqs_by_section(self, sections: Union[int, List[int]], show_numbers: bool=True) -> str:
        word_freq_lists = self.get_word_freqs_by_section(sections)

        pretty_print_by_section = list(map(lambda word_freqs: self._pretty_print_freq_list(word_freqs, show_numbers), word_freq_lists))

        final_pretty_print = []

        section_indices = sections if type(sections) == list else list(range(0, self.num_pages // sections))

        for i in range(len(pretty_print_by_section)):

            final_pretty_print.append(f"\n\n---\n\n# {section_indices[i]}-{section_indices[i+1]}\n\n")
            final_pretty_print.append(pretty_print_by_section[i])

        return final_pretty_print



if __name__ == "__main__":
    assert len(sys.argv) == 2, "Must provide exactly one argument."

    filepath = sys.argv[1]


    zipf_reader = ZipfReader(filepath)

    #print(zipf_reader.pretty_print_word_freqs())
    print(*zipf_reader.pretty_print_word_freqs_by_section([2, 3, 4], False))
