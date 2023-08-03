from importlib import import_module


PARSERS = {}
CLEANERS = {}

for language in ["de", "en", "fr", "it"]:
    module = import_module("extract.lang." + language)
    PARSERS[language] = module.parse
    CLEANERS[language] = module.clean


def get_parser(language):
    return PARSERS[language]


def get_cleaner(language):
    return CLEANERS[language]
