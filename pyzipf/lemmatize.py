import os
from typing import Dict, List, Union
from collections import Counter

import spacy

from zipfify import ZipfReader


LANGUAGES = [
    "zh",
    "da",
    "nl",
    "en",
    "de",
    "el",
    "it",
    "ja",
    "lt",
    "mk",
    "xx", # multi-language
    "nb",
    "pl",
    "pt",
    "ro",
    "ru",
    "es"
]

LANGUAGE_DATASETS = {
    "zh": "zh_core_web_sm",
    "da": "da_core_news_sm",
    "nl": "nl_core_news_sm",
    "en": "en_core_web_sm",
    "de": "de_core_news_sm",
    "el": "el_core_news_sm",
    "it": "it_core_news_sm",
    "ja": "ja_core_news_sm",
    "lt": "lt_core_news_sm",
    "mk": "mk_core_news_sm",
    "xx": "xx_ent_wiki_sm", # multi-language
    "nb": "nb_core_news_sm",
    "pl": "pl_core_news_sm",
    "pt": "pt_core_news_sm",
    "ro": "ro_core_news_sm",
    "ru": "ru_core_news_sm",
    "es": "es_core_news_sm"
}


class LemmaZipfReader(ZipfReader):
    def __init__(self, filepath: Union[str, "os.PathLike[Any]"], language: str="en"):
        ZipfReader.__init__(self, filepath)
        self.language = language

        ignore_relpath = f"ignore/{language}.txt"
        ignore_path = os.path.join(os.getcwd(), ignore_relpath)
        if os.path.isfile(ignore_path):
            with open(ignore_path, "r") as f:
                self.ignore = list(map(lambda s: s.strip(), f.readlines()))

        else:
            self.ignore = []

        try:
            self.nlp = spacy.load(self.nlp_dataset)
        except OSError:
            raise OSError(f"You must first download the spaCy model `{language}_core_news_sm`. To do so, run `python -m spacy download {language}_core_news_sm`")

    def page_range_to_word_freqs(self, initial_page: int, final_page: int) -> Counter:
        word_counter = super().page_range_to_word_freqs(initial_page, final_page)

        for word in self.ignore:
            del word_counter[word]

        return word_counter

    @property
    def nlp_dataset(self):
        # TODO: Offer more customizability in language dataset selection
        return LANGUAGE_DATASETS[self.language]


    def preprocess(self, word_list: List[str]) -> List[str]:
        """
        This is used by Lemma Zipf Readers to reduce words to their lemma forms.
        """

        return list(map(lambda token: token.lemma_, self.nlp(" ".join(word_list))))
