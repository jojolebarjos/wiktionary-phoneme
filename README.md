
# Wiktionary IPA Dataset

First, download the desired Wiktionary dump, from [this repository](https://dumps.wikimedia.org/). For instance, here are the latest links for some languages:

 * [English](https://dumps.wikimedia.org/enwiktionary/latest/enwiktionary-latest-pages-articles.xml.bz2)
 * [French](https://dumps.wikimedia.org/frwiktionary/latest/frwiktionary-latest-pages-articles.xml.bz2)
 * [German](https://dumps.wikimedia.org/dewiktionary/latest/dewiktionary-latest-pages-articles.xml.bz2)
 * [Italian](https://dumps.wikimedia.org/itwiktionary/latest/itwiktionary-latest-pages-articles.xml.bz2)

Then, run the following command to extract the IPA data:

```
python -m extract frwiktionary-latest-pages-articles.xml.bz2 fr.tsv
```

Note that you can disable the cleaning step to get all detected entries:

```
python -m extract -r frwiktionary-latest-pages-articles.xml.bz2 fr.raw.tsv
```

The output is easily loaded and processed using `pandas`:

```python
import pandas as pd

fr_df = pd.read_csv("fr.tsv", sep="\t", na_filter=False)

sorted_fr_df = fr_df.sort_values(["text", "pronunciation", "language"]).drop_duplicates()
sorted_fr_df.to_csv("fr.sorted.tsv", index=False, sep="\t", encoding="utf-8", line_terminator="\n")
```
