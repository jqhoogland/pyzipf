import sys, os
from typing import Union, List, Tuple
from collections import Counter

from PyPDF2 import PdfFileReader

PUNCTUATIONS = """!()[]{};:\"\,<>\./?@#$%^&;*_~™«»"""
CONSONANTS = "BCDFGHJKLMNPQRSTVWXZ"

class ZipfReader:
    def __init__(self, filepath: Union[str, "os.PathLike[Any]"]):
        self.filepath = filepath
        self.pdf_reader = PdfFileReader(filepath)

    @property
    def num_pages(self):
        return self.pdf_reader.numPages

    def preprocess(self, word_list: List[str]) -> List[str]:
        """
        This is used by Lemma Zipf Readers to reduce words to their lemma forms.
        """
        return word_list

    def page_to_word_list(self, page_index: int=0) -> List[str]:
        page = self.pdf_reader.getPage(page_index)

        raw_text = page.extractText()

        # First we replace line breaks with spaces, get rid of empty lines, and convert to lowercase

        dense_text = raw_text.replace("\n", "").lower()

        # 1. ``extractText`` often omits spaces at line breaks.
        #    - Wherever we see a digit, we skip.
        #    - Wherever we see an uppercase directly following a lowercase, we insert a space.
        #    - Wherever we see a hyphen denoting continuing (e.g. "some\n-thing"), we rejoin.
        # 2. We also remove all punctuation and numbers (replacing this with spaces)
        # TODO: remove urls
        # TODO: Count ' differently (e.g. "dell'importanza" -> "dell'", "importanza" or something similar)
        # TODO: Roman numerals

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
        cleaned_list = list(filter(lambda word: len(word) > 0 and word not in CONSONANTS, raw_list))

        return self.preprocess(cleaned_list)


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

    def get_word_freqs_by_section(self, sections: Union[int, List[int]], show_duplicates: bool=False) -> List[Counter]:
        """
        ``sections`` is either:
        1. An int for the number of pages per section, or
        2. A list of the indicies of the first page of every section.

        If show_duplicates is false, we only count a word in the first section we encounter it.
        Otherwise, we separately count its occurences in each section.
        NOTE: The count for any word will still only be the count within that particular section.
        """
        global_counter = Counter()
        word_freq_lists = []

        section_indices = sections if type(sections) == list else list(range(0, self.num_pages, sections))

        for i in range(len(section_indices) - 1):
            # TODO: Test
            section_counter = self.page_range_to_word_freqs(section_indices[i], section_indices[i + 1])

            if not show_duplicates:
                for word in global_counter.keys():
                    global_counter[word] += section_counter[word]
                    # We set the already encountered word counts to 0, then remove non-positive count items with unary addition.
                    section_counter[word] = 0

                global_counter += section_counter


            word_freq_lists.append(+section_counter)

        return word_freq_lists


    def _pretty_print_freq_list(self, word_freqs: Counter, show_numbers: bool=True) -> str:
        word_freq_tuples = word_freqs.most_common()

        if show_numbers:
            return "".join(list(map(lambda wordfreq: f"{wordfreq[0].strip()} {wordfreq[1]}\n", word_freq_tuples)))

        return "".join(list(map(lambda wordfreq: f"{wordfreq[0].strip()}\n", word_freq_tuples)))


    def pretty_print_word_freqs(self, show_numbers: bool=True) -> str:
        word_freqs = self.get_word_freqs()

        return self._pretty_print_freq_list(word_freqs, show_numbers)

    def pretty_print_word_freqs_by_section(self, sections: Union[int, List[int]], show_numbers: bool=True, show_duplicates: bool=False) -> str:
        word_freq_lists = self.get_word_freqs_by_section(sections, show_duplicates)

        pretty_print_by_section = list(map(lambda word_freqs: self._pretty_print_freq_list(word_freqs, show_numbers), word_freq_lists))

        final_pretty_print = []

        section_indices = sections if type(sections) == list else list(range(0, self.num_pages, sections))

        for i in range(len(pretty_print_by_section)):

            final_pretty_print.append(f"\n\n---\n\n# {section_indices[i]}-{section_indices[i+1]}\n\n---\n")
            final_pretty_print.append(pretty_print_by_section[i])

        return final_pretty_print
