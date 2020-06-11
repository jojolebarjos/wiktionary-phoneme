
import regex as re


#
# There should always be a language header, using the following format:
#   == {{langue|fr}} ==
#   == {{langue|fro}} ==
#   == {{langue|en}} ==
#   == {{langue|yue}} ==
#
# In some VERY RARE cases, they insert the language directly:
#   == Latin ==
#


#
# Then, there should be a section header:
#   === {{S|nom|fr|num=2}} ===
#   === {{S|nom|ja|num=2|clé=か}} ===
#   === {{S|nom|yue}} ===
#   === {{S|prononciation}} ===
#


#
# The most common template for pronunciation (may be empty):
#   {{pron|u.vʁaʒ|fr}}
#   {{pron||ko-Hani}}
#   
# Possibly with prefixed text:
#   '''penguin''' {{pron|ˈpɛŋ.ɡwɪn|en}}
#   '''ouvrage''' {{pron|u.vʁaʒ|fr}}
#   '''militaire''' {{pron|mi.li.tɛʁ|fr}} {{mf}}
#
# Or as a suffix:
#   {{standard|nocat=1}} {{pron|ʒə sɥi|fr}} ''(je suis)''
#
# There might also be notes/specializations:
#   Canada : {{pron|ʃɛːz|fr}}, {{phon|ʃaɛ̯z|fr}}
#   Français méridional : {{pron|ˈʃɛ.zə|fr}}
#   Encore parfois prononcé irrégulièrement {{pron|mɛ.kʁə.di|fr}}
#   '''travail''' {{pron|ˈtʁæ.veɪl|en}} ou {{pron|tɹə.ˈveɪl|en}}
#
# Note that a close template is used in the same way:
#   {{phon|ʁɛ̃ːn|fr}}
#
# Finally, note that some expansion might be attached:
#   '''al''' {{prononcé|année-lumière|fr}} {{pron|a.ne ly.mjɛʁ|fr}} {{f}}.
#   '''cf.''' {{pron|kɔ̃.fɛʁ|fr}} {{prononcé|confère|fr}} <small>ou</small> {{pron|se.ɛf|fr}} {{invar}}
#   :* '''cinq minutes''' {{pron|sɛ̃ mi.nyt|fr}}
#
# And that some of them are not desired:
#   * '''cantonnais''' {{pron|sɛːŋ⁵⁵|yue}},
#


#
# Audio clips are also commonplace:
#   {{écouter|lang=fr|Canada {{popu|nocat=1}}|maŋ.ɡɔ|fr}}
#   {{écouter|Québec|lang=fr|sjaɪʒ}}
#
# Note that the actual content might differ from the page title, which should be annotated:
#   {{écouter|lang=fr|France (Paris)|ɛ̃.n‿u.vʁaʒ|audio=Fr-ouvrage.ogg|titre=un ouvrage}}
#   {{écouter|France (Paris)|lø bœʁ|audio=Fr-beurre.ogg|titre=le beurre|lang=fr}}
#


# 
# Part-of-speech is often specified as well, possibly including one or multiple pronunciations:
#   {{fr-rég|sjɛʒ}}
#   {{fr-inv|se.de.ʁɔm|sp=1}}
#   {{en-nom-rég|ˈpɛŋ.gwɪn}}
#   {{en-nom|fish|fish|p2=fishes|fɪʃ|fɪʃ|pp2=fɪʃ.ɪz}}
#   {{en-conj-rég-s|inf.pron=fɪʃ|pp.psuf=t}}
#   {{de-nom-m-s-e|ˈmɪt.vɔx|gs2=Mittwoches|ds2=Mittwoche}}
#   {{de-nom-m-s-e|ˈdɔnɐstaːk|ˈdɔnɐstaːɡə|gs2=Donnerstages|ds2=Donnerstage}}
#
# Note that some variations are present, and not trivially mapped:
#   {{fr-accord-en|ɛs.tɔ.nj}}
#


#
# It seems that there are minor templates as well:
#   | trois œufs || {{pron-API|/tʁwa.'''zø'''/}}
#


#
# Derivatives:
#   ''un flux abondant'' peut se prononcer {{pron|œ̃ fly.z‿a.bɔ̃.dɑ̃|fr}}{{R|Littré}}.
#


#
# In conclusion:
#  * There is almost always the full entry (e.g. '''ouvrage''' {{pron|u.vʁaʒ|fr}} structure)
#  * The PoS ones are almost always redundant (e.g. {{fr-rég|sjɛʒ}}), and can be ignored
#  * Audio clips often add alternative pronunciations, and sometimes a slight variation (i.e. titre)
#

pron_long_r = re.compile(r"^\s*'''([^\{]*)'''\s*\{\{pron\|([^\|]*)\|([^\}]*)\}\}")
# TODO handle {{prononcé

comment_r = re.compile(r"<!\-\-.*?\-\->", re.DOTALL)
bracket_r = re.compile(r"\{\{|\}\}")
ecouter_r = re.compile(r"\{\{écouter\|")

# TODO écouter
# TODO get regional pronunciation


def parse(title, content):

    # First, strip any HTML/XML comment
    content = comment_r.sub("", content)

    # Then, collect using various strategies
    results = set()
    for text, language, pronunciation in from_any(title, content):

        # Basic cleaning
        text = text.strip()
        language = language.strip()
        pronunciation = pronunciation.strip()

        # Only keep complete results
        if text and language and pronunciation:
            result = text, language, pronunciation
            results.add(result)

    return results


def from_any(title, content):
    yield from from_entries(title, content)
    yield from from_audio_clips(title, content)


def from_entries(title, content):
    for line in content.split("\n"):

        match = pron_long_r.search(line)
        if match is not None:
            text = match.group(1)
            pronunciation = match.group(2)
            language = match.group(3)
            yield text, language, pronunciation


def from_audio_clips(title, content):
    # TODO parse audio clips
    return []


def iterate_audio_clips(content):
    """Iterate over ``{{écouter|...}}`` templates."""

    pos = 0
    while True:

        # Search for next clip
        match = ecouter_r.search(content, pos=pos)
        if not match:
            break

        # As there might be nested templates, and also multiple clips on the
        # same line, we need to count opening and closing brackets
        start = match.start()
        pos = match.end()
        depth = 1
        while depth > 0:
            bracket = bracket_r.search(content, pos=pos)

            # Maybe the template is not properly closed
            if not bracket:
                pos = len(content)
                break

            # Move forward
            pos = bracket.end()
            bracket = bracket.group()
            if bracket == "{{":
                depth += 1
            else:
                depth -= 1

        end = pos
        yield content[start:end]
