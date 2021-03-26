# PyZipf

In natural language corpora, word frequencies follow a power-law distribution (with exponent typically close to 1). This is known as [Zipf's law](https://en.wikipedia.org/wiki/Zipf%27s_law).

For language learners, knowing the word frequency list gives us an advantage: we can focus on the most common words to get the most bang for our lanaguage-learning buck. For example, in the Brown Corpus (of American English), you only need 135 "words" to recover half of the corpus.

For reference, Wiktionary has an [excellent collection of frequency lists](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists).

However, when we're interested in reading a specific piece of literature in a target language, focusing on the overall frequency list may not be ideal. It would be better to focus on the word frequency list for that particular resource.

With PyZipf you can easily convert pdfs into word lists for this purpose. Start with the most common words, in the first pages, to understand as efficiently as possible.

### How to use
Run ``python pyzipf --help`` to get an overview of the options.


### Lemma frequency lists
Ideally, you have some grasp of the grammar, in which case it suffices to learn the lemmas (i.e. root words).


### Ignoring words
You can put words you already know in `/ignore/[langcode].txt`, and these will be ignored when crawling new sources.
Here `[langcode]` is the 2-letter code for your target language (e.g., `it`, `en`, `es`).

As a start, I've included `/ignore/it-1000.txt` which has the 1000 most common words in Italian ([source](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Italian1000))You can directly copy this into `/ignore/it.txt` to jump ahead with your italian.

In the future, I'll be adding freq lists for other languages so you have an easier time jumping ahead.

Whenever you finish a new resource, make sure to add your newly learned vocab to the end of the relevant `/ignore/[langcode].txt` file. This way you won't have to encounter words a second time.
