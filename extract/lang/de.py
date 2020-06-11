
import regex as re


#
# Definitions start with the name and the language:
#   == Liebe ({{Sprache|Deutsch}}) ==
#

header_r = re.compile(r"\s*==\s*[^=]*?\s*\(\s*\{\{Sprache\|([^\}]*)\}\}\s*\)\s*==\s*")


#
# Common pronunciation definition
#   {{Aussprache}}
#   :{{IPA}} {{Lautschrift|aˈpʀɪl}}
#   :{{IPA}} {{Lautschrift|ˈɔʁdoː}}, {{Pl.}} {{Lautschrift|ˈɔʁdineːs}}
#   :{{IPA}} ''östlich:'' {{Lautschrift|səˈɾiə}}, ''westlich:'' {{Lautschrift|seˈɾia}}
#   :{{IPA}} {{Lautschrift|ˈtʀiːbʊs}}, &lt;!-- Spezialfall, NICHT löschen --&gt;{{Pl.1}} {{Lautschrift|ˈtʀiːbuːs}}
#

ipa_r = re.compile(r"\:\{\{IPA\}\}\s*\{\{Lautschrift\|([^\}]+)\}\}")


# German names to ISO 639-1 Codes (used by Wikipedia)
LANGUAGES = {
    'Deutsch' : 'de',
    'Englisch' : 'en',
    'Französisch' : 'fr',
    'Italienisch' : 'it',
    'Latein' : 'la',
    'Spanisch' : 'es',
}


def parse(title, content):

    language = ""
    for line in content.split("\n"):
    
        # Check for header, update current word and language
        match = header_r.search(line)
        if match is not None:
            language = match.group(1)
            language = LANGUAGES.get(language, "")

        # Check standard pronunciation definition
        match = ipa_r.search(line)
        if match is not None:
            pronunciation = match.group(1)
            # TODO check if we need to use the header word instead
            yield title, language, pronunciation
