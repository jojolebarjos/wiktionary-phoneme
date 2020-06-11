
from .de import parse as parse_de
from .en import parse as parse_en
from .fr import parse as parse_fr
from .it import parse as parse_it


PARSERS = {
    'de': parse_de,
    'en': parse_en,
    'fr': parse_fr,
    'it': parse_it,
}


def get_parser(language):
    return PARSERS[language]
