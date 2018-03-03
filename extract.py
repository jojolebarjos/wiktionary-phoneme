# -*- coding: utf-8 -*-


import io
import os
import bz2
from lxml import etree
from tqdm import tqdm
import re
import csv


#
# English-specific parser
#

# Common pronunciation definition
# * {{a|RP}} {{IPA|/pɔːtˈmæn.təʊ/|lang=en}}
# * {{a|US}} {{enPR|pôrtmă'ntō}}, {{IPA|/pɔːɹtˈmæntoʊ/|lang=en}}; {{enPR|pô'rtmăntōʹ}}, {{IPA|/ˌpɔːɹtmænˈtoʊ/|lang=en}}
# * {{a|Portugal}} {{IPA|/ˈfɾɐj/|/ˈfɾej/|lang=pt}}
# * {{a|US|UK}} {{IPA|/kæt/|[kʰæt]|[kʰæt̚]|lang=en}}
# * {{a|Munster|Aran}} {{IPA|/kɑt̪ˠ/|lang=ga}}
r_en_ipa = re.compile(r'\{\{IPA\|\/([^\/]*)\/.*?(?:lang=([^\}]*))?\}\}', re.UNICODE)

# Extract phonemes from the whole article
def parse_en(title, text):
  
  # Iterate over lines
  results = []
  for line in text.split('\n'):
    
    # Check standard pronunciation definition
    match = r_en_ipa.search(line)
    if match is not None:
      pronunciation = match.group(1)
      language = match.group(2) or ''
      result = (title, language, pronunciation)
      results.append(result)
  
  # Ready
  return results


#
# French-specific parser
#

# Common pronunciation definition
# * {{pron|ʃɛz|fr}}
# TODO

# Common pronunciation definition, with text
# '''lire''' {{pron|liʁ|fr}}
# '''manga''' {{pron|mɑ̃.ɡa|fr}}
r_fr_pron_long = re.compile(r'\'\'\'([^\{]*)\'\'\'\s*\{\{pron\|([^\|]*)\|([^\}]*)\}\}', re.UNICODE)

# Alternative pronunciation definition
# {{fr-rég|mœbl}}
# {{en-nom-rég|ˌɑː(ɹ)m.ˈtʃeə(ɹ)}}
# TODO r_fr_reg = re.compile(r'\{\{([^\-]*)\-[^\|]*rég\|([^\}]*)\}\}', re.UNICODE)


# Extract phonemes from the whole article
def parse_fr(title, text):
  
  # Iterate over lines
  results = []
  for line in text.split('\n'):
    
    # Check standard pronunciation definition
    match = r_fr_pron_long.search(line)
    if match is not None:
      text = match.group(1)
      pronunciation = match.group(2)
      language = match.group(3)
      result = (text, language, pronunciation)
      results.append(result)
  
  # Ready
  return results
  

#
# German-specific parser
#

# Word/language header
#   == Liebe ({{Sprache|Deutsch}}) ==
r_de_header = re.compile(r'\s*==\s*[^=]*?\s*\(\s*\{\{Sprache\|([^\}]*)\}\}\s*\)\s*==\s*', re.UNICODE)

# Common pronunciation definition
#   {{Aussprache}}
#   :{{IPA}} {{Lautschrift|aˈpʀɪl}}
#   :{{IPA}} {{Lautschrift|ˈɔʁdoː}}, {{Pl.}} {{Lautschrift|ˈɔʁdineːs}}
#   :{{IPA}} ''östlich:'' {{Lautschrift|səˈɾiə}}, ''westlich:'' {{Lautschrift|seˈɾia}}
#   :{{IPA}} {{Lautschrift|ˈtʀiːbʊs}}, &lt;!-- Spezialfall, NICHT löschen --&gt;{{Pl.1}} {{Lautschrift|ˈtʀiːbuːs}}
r_de_ipa = re.compile(r'\:\{\{IPA\}\}\s*\{\{Lautschrift\|([^\}]+)\}\}', re.UNICODE)

# German names to ISO 639-1 Codes (used by Wikipedia)
m_de_languages = {
  'Englisch' : 'en',
  'Französisch' : 'fr',
  'Deutsch' : 'de',
  'Italienisch' : 'it',
  'Latein' : 'la',
  'Spanisch' : 'es'
  # TODO handle more language codes
}

# Extract phonemes from the whole article
def parse_de(title, text):
  
  # Iterate over lines
  language = ''
  results = []
  for line in text.split('\n'):
    
    # Check for header, update current word and language
    match = r_de_header.search(line)
    if match is not None:
      language = match.group(1)
      language = m_de_languages.get(language, '')
    
    # Check standard pronunciation definition
    match = r_de_ipa.search(line)
    if match is not None:
      pronunciation = match.group(1)
      result = (title, language, pronunciation)
      results.append(result)
  
  # Ready
  return results


#
# Italian-specific
#

# Language header
# == {{-it-}} ==
# == {{-la-}} ==
r_it_header = re.compile(r'\s*==\s*\{\{\-(.*?)\-\}\}\s*==\s*', re.UNICODE)

# Common pronunciation definition
# * {{IPA|/ˈkaː.za/|/ˈkaː.sa/}}
# {{IPA|/inforˈmatika/}}
# {{IPA|/'libero/}}
r_it_ipa = re.compile(r'\{\{IPA\|\/(.*?)\/.*?\}\}', re.UNICODE)

# Extract phonemes from the whole article
def parse_it(title, text):

  # Iterate over lines
  language = ''
  results = []
  for line in text.split('\n'):
    
    # Check for header, update current word and language
    match = r_it_header.search(line)
    if match is not None:
      language = match.group(1)
    
    # Check standard pronunciation definition
    match = r_it_ipa.search(line)
    if match is not None:
      pronunciation = match.group(1)
      result = (title, language, pronunciation)
      results.append(result)
  
  # Ready
  return results


#
# Main process
#

# Get local directory
here = os.path.dirname(os.path.realpath(__file__))

# Iterate over pages in a BZ2 Wikipedia/Wiktionary dump
def iterate(path):
  with bz2.open(path) as file:
    title = None
    ns = None
    text = None
    
    # For each node
    for action, elem in etree.iterparse(file):
      tag = elem.tag
      if '}' in tag:
        tag = tag[tag.rindex('}') + 1:]
      
      # Keep relevant information
      if tag == 'title':
        title = elem.text
      elif tag == 'ns':
        ns = elem.text
      elif tag == 'text':
        text = elem.text
      
      # When a page is complete, export it
      elif tag == 'page':
        if title is not None and ns == '0' and text is not None:
          yield title, text
        title = None
        ns = None
        text = None
        
        # Free memory
        del elem.getparent()[0]

# Process Wiktionary dump and extract phonetic information
def process(lang):
  
  # Select parser
  parse = {
    'en' : parse_en,
    'fr' : parse_fr,
    'de' : parse_de,
    'it' : parse_it
  }[lang]
  
  # Assume latest dump in same directory
  input_path = os.path.join(here, '%swiktionary-latest-pages-articles.xml.bz2' % lang)
  
  # Open output CSV file
  output_path = os.path.join(here, '%s.csv' % lang)
  with io.open(output_path, 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['WORD', 'LANGUAGE', 'PRONUNCIATION'])
    
    # Stream and parse input dump
    for title, text in tqdm(iterate(input_path)):
      results = parse(title, text)
      results = {result for result in results if result[2] != ''}
      for result in sorted(results):
        writer.writerow(result)

# Standalone usage does the export process
if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Extract phonemes from Wiktionary BZ2 dump.')
  parser.add_argument('language', help='language code (en, fr, de, it)')
  args = parser.parse_args()
  process(args.language)
