
# Phonemes from Wiktionary

Phonetic notation is automatically extracted from [Wiktionary dumps](https://dumps.wikimedia.org/). As each language have its notation, only [English](https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2), [French](https://dumps.wikimedia.org/frwiktionary/latest/frwiktionary-latest-pages-articles.xml.bz2), [German](https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-articles.xml.bz2) and [Italian](https://dumps.wikimedia.org/itwiktionary/latest/itwiktionary-latest-pages-articles.xml.bz2) are supported (yet). However, additional languages may be partially available, as Wiktionary often defines terms in other languages.

```
pip install lxml tqdm
wget https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2
python extract.py en
```
