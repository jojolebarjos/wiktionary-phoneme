import regex as re


#
# The most common template for pronunciation (may be empty):
#   {{a|RP}} {{IPA|/pɔːtˈmæn.təʊ/|lang=en}}
#   {{a|US}} {{enPR|pôrtmă'ntō}}, {{IPA|/pɔːɹtˈmæntoʊ/|lang=en}}; {{enPR|pô'rtmăntōʹ}}, {{IPA|/ˌpɔːɹtmænˈtoʊ/|lang=en}}
#   {{a|Portugal}} {{IPA|/ˈfɾɐj/|/ˈfɾej/|lang=pt}}
#   {{a|US|UK}} {{IPA|/kæt/|[kʰæt]|[kʰæt̚]|lang=en}}
#   {{a|Munster|Aran}} {{IPA|/kɑt̪ˠ/|lang=ga}}
#

ipa_r = re.compile(r"\{\{IPA\|\/([^\/]*)\/.*?(?:lang=([^\}]*))?\}\}")


# TODO explore more patterns


def parse(title, content):
    # TODO handle tags

    for line in content.split("\n"):

        match = ipa_r.search(line)
        if match is not None:
            pronunciation = match.group(1)
            language = match.group(2) or ""
            # TODO check that pronunciation is always associated to title
            yield title, language, "", pronunciation
