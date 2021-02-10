# PyZipf

In natural language corpora, word frequencies follow a power-law distribution (with exponent typically close to 1). This is known as [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law).

For language learners, knowing the word frequency list gives us an advantage: we can focus on the most common words to get the most bang for our buck. For example, in the Brown Corpus (of American English), you only need 135 "words" to recover half of the corpus.

For reference, Wiktionary has an [excellent collection of frequency lists](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists).

However, when we're interested in reading specialized literature in a target language, focusing on the overall frequency list may not be ideal. It would be better to focus on the word frequency list for that resource.

With PyZipf you can easily convert pdfs into word lists for this purpose.

### How to use
Run ``python pyzipf --help`` to get an overview of the options.


### Lemma frequency lists
Ideally, you have some grasp of the grammar, in which case it suffices to learn the lemmas (i.e. root words).


I'm currently learning Italian, so that's the only lemmatizer I've set up (with the help of spaCy). But it's easy to extend this to other languages so stay tuned.
