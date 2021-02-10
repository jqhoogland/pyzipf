from typing import Dict, List
from collections import Counter

import spacy

from zipfify import ZipfReader

nlp = spacy.load('it_core_news_sm')

class ItalianLemmatizedReader(ZipfReader):

    def preprocess(self, word_list: List[str]) -> List[str]:
        """
        This is used by Lemma Zipf Readers to reduce words to their lemma forms.
        """

        return list(map(lambda token: token.lemma_, nlp(" ".join(word_list))))
