import sys, os
from typing import Union, List, Dict
from collections import Counter

from PyPDF2 import PdfFileReader

PUNCTUATIONS = """!()[]{};:\"\,<>\./?@#$%^&;*_~"""
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


    def page_range_to_word_frequencies(self, initial_page: int, final_page: int) -> Dict[str, int]:
        word_counter = Counter()

        # If ``final_page`` is greater than the number of pages in the document, we take the document length instead.
        for page_index in range(min(self.num_pages, final_page)):
            word_list = self.page_to_word_list(page_index)

            for word in word_list:
                word_counter[word] += 1

        return word_counter.most_common(100)


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Must provide exactly one argument."

    filepath = sys.argv[1]


    zipf_reader = ZipfReader(filepath)

    print(zipf_reader.page_range_to_word_frequencies(0, 20))
