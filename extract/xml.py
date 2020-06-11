
import bz2

from lxml import etree


def iterate_dump(file):
    """Stream markup articles."""

    # Wiktionary dumps are BZ2 XML files
    with bz2.open(file) as archive:

        # We only look at a few XML fields
        title = None
        ns = None
        text = None

        # Stream to avoid memory growth
        for action, elem in etree.iterparse(archive):

            # Quick and dirty hack to disregard XML namespaces...
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
