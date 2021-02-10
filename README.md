# PyZipf

In natural language corpora, word frequencies follow a power-law distribution (with exponent typically close to 1). This is known as [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law).

For language learners, knowing the word frequency list gives us an advantage: we can focus on the most common words to get the most bang for our buck. For example, in the Brown Corpus (of American English), you only need 135 "words" to recover half of the corpus.

For reference, Wiktionary has an [excellent collection of frequency lists](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists).

However, when we're interested in reading specialized literature in a target language, focusing on the overall frequency list may not be ideal. It would be better to focus on the word frequency list for that resource.

With PyZipf you can easily convert pdfs into word lists for this purpose.

### Note
- This currently does not identify distinct lemmas (i.e., root words). So "go", "goes", and "went" would show up as distinct in an English text. I will work on expanding this functionality in the future
- I'm planning on including the functionality to create a word list per chapter. So you can start reading before you've mastered all the vocabulary.
