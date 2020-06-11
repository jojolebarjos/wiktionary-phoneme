
# Wiktionary IPA Dataset

First, download the desired Wiktionary dump, from [this repository](https://dumps.wikimedia.org/). For instance, here are the latest links for some languages:

 * [English](https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2)
 * [French](https://dumps.wikimedia.org/frwiktionary/latest/frwiktionary-latest-pages-articles.xml.bz2)

Then, run the following command to extract the raw IPA data:

```
python -m extract enwiktionary-latest-pages-articles.xml.bz2 en.raw.tsv
```
