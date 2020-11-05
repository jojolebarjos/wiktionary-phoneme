
import regex as re


#
# There should always be a language header, using the following format:
#   == {{-it-}} ==
#   == {{-la-}} ==
#

header_r = re.compile(r"\s*==\s*\{\{\-(.*?)\-\}\}\s*==\s*")


#
# Common pronunciation definition:
#   * {{IPA|/ˈkaː.za/|/ˈkaː.sa/}}
#   {{IPA|/inforˈmatika/}}
#   {{IPA|/'libero/}}
#

ipa_r = re.compile(r"\{\{IPA\|\/(.*?)\/.*?\}\}")


def parse(title, content):
    # TODO handle tags

    language = ""
    for line in content.split("\n"):
    
        # Check for header, update current word and language
        match = header_r.search(line)
        if match is not None:
            language = match.group(1)
    
        # Check standard pronunciation definition
        match = ipa_r.search(line)
        if match is not None:
            pronunciation = match.group(1)
            yield title, language, "", pronunciation
