import sys, os
from typing import Union, List, Dict

from PyPDF2 import PdfFileReader

PUNCTUATIONS = """!()[]{};:\"\,<>\./?@#$%^&;*_~"""

class ZipfReader:
    def __init__(self, filepath: Union[str, "os.PathLike[Any]"]):
        self.filepath = filepath
        self.pdf_reader = PdfFileReader(filepath)

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

        # Get rid of nonce words (i.e., empty strings)
        # TODO: Include minimum word length
        cleaned_list = list(filter(lambda word: len(word) > 0, raw_list))

        return cleaned_list

    def page_to_word_frequencies(self, page_index: int=0) -> Dict[str, int]:
        pass

    def document_to_word_frequencies(self) -> Dict[str, int]:
        pass


if __name__ == "__main__":
    assert len(sys.argv) == 2, "Must provide exactly one argument."

    filepath = sys.argv[1]


    zipf_reader = ZipfReader(filepath)

    print(zipf_reader.page_to_word_list(10))
