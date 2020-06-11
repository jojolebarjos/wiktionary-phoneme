
import regex as re


TEXT_REPLACEMENT = {

    # Unify whitespace
    "\xa0": " ",
    "&nbsp;": " ",

    # Unify apostrophes
    "’": "'",
    "&#39;": "'",

    # Unify symbols
    "&amp;": "&",
    
    # TODO split ligatures? æ, œ
}


TEXT_WHITELIST = " .,-'aàâäbcçdeéèêëfghiîïjklmnoôöpqrstuùûüvwxyz"
# TODO digits? about 750 entries
# TODO uncommon symbols? e.g. &, €, +


TEXT_PREFIX_BLACKLIST = [
    "'",
    "-",
    ".",
]


def clean_text(text):

    # Replace according to mapping
    for a, b in TEXT_REPLACEMENT.items():
        text = text.replace(a, b)

    # Empty text is ignored
    text = text.strip()
    if not text:
        return None

    # Discard any entry with unexpected symbol
    chars = set(text.lower())
    chars.difference_update(TEXT_WHITELIST)
    if chars:
        return None

    # Ignore some prefixes
    for prefix in TEXT_PREFIX_BLACKLIST:
        if text.startswith(prefix):
            return None

    return text


IPA_REPLACEMENT = {
    
    # Ignore stress marker (not sufficiently used)
    "ˈ": "",
    "'": "",
    
    # Unify interpunct
    '·': '.',
    '-': '.',

    # Replace incorrect symbols with their IPA equivalent
    "à": "a",
    "ε": "ɛ",
    "é": "e",
    "ǝ": "ə",
    "r": "ʁ",
    "ʀ": "ʁ",
    "ɾ": "ʁ",
    "c": "k",
    "g": "ɡ",
    "ᴐ": "ɔ",
    # TODO "h": "ʔ",
    
    # Tilde-related errors
    "ã": "ɑ\u0303",
    "\u0303ɑ": "ɑ\u0303",
    "ẽ": "ɛ\u0303",
    "\u0303ɛ": "ɛ\u0303",
    "\u0303œ": "œ\u0303",
    "\u0303ɔ": "ɔ\u0303",
}


IPA_WHITELIST = {
    # See
    #   https://en.wikipedia.org/wiki/French_phonology
    #   https://en.wikipedia.org/wiki/Help:IPA/French
    
    # Punctuation
    ' ',
    '.',
    'ː',
    '\u203f',
    '͡',
    '(', ')',
    
    # Consonants
    "m", "n", "ɲ", "ŋ",
    "p", "t", "k",
    "b", "d", "ɡ",
    "f", "s", "ʃ",
    "v", "z", "ʒ", "ʁ",
    "l", "j",
    "ɥ", "w",
    
    # Oral vowels
    "i", "y", "u",
    "e", "ø", "ə", "o",
    "ɛ", "ɛː", "œ", "ɔ",
    "a", "ɑ",
    
    # Nasal vowels
    "ɛ̃", "œ̃", "ɔ̃",
    "ɑ̃",
    
    # Glottal sounds
    "h", "ʔ",
    
    # TODO English?
    #   "ʌ", # just
    #   "ʊ", # hook, foot
    #   "ɹ", # red
    #   "ɪ", # bit
}


def _list_to_regex(tokens):
    parts = []
    for token in sorted(tokens):
        for c in "\\.()-?*+[]{} ":
            token = token.replace(c, "\\" + c)
        parts.append(token)
    pattern = "(?:" + "|".join(parts) + ")+"
    return re.compile(pattern)

IPA_WHITELIST_R = _list_to_regex(IPA_WHITELIST)


def clean_pronunciation(pronunciation):

    # Discard choices
    if " ou " in pronunciation:
        return None

    # Strip boundary markers
    pronunciation = pronunciation.strip("/\\{|}")

    # Lowercase to remove small errors
    pronunciation = pronunciation.lower()

    # Apply replacements
    for a, b in IPA_REPLACEMENT.items():
        pronunciation = pronunciation.replace(a, b)

    # Discard any entry with unexpected symbol
    if IPA_WHITELIST_R.fullmatch(pronunciation) is None:
        return None

    return pronunciation


def clean(text, language, pronunciation):

    # Currently ignoring anything that is not French
    if language != "fr":
        return None

    # Clean text
    text = clean_text(text)
    if text is None:
        return None

    # Clean pronunciation
    pronunciation = clean_pronunciation(pronunciation)
    if pronunciation is None:
        return None

    return text, language, pronunciation
