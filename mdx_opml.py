"""
OPML Extension
=============

Summary
-------

An extension to Python-Markdown that outputs a markdown document as OPML.

derive from mdx_rss.py

Each item in the OPML document is a link.

Usage
-----

From the Python interpreter:

    >>> import markdown
    >>> text = "Some markdown document."
    >>> opml = markdown.markdown(text, ['opml'])

Configuring the Output
----------------------

An RSS document includes some data about the document (URI, author, title) that
will likely need to be configured for your needs. Therefore, three configuration
options are available:

* **URL** : The Main URL for the document.
* **CREATOR** : The Feed creator's name.
* **TITLE** : The title for the feed.

An example:

    >>> opml = markdown.markdown(text, extensions = \
    ...        ['opml(URL=http://example.com,CREATOR=JOHN DOE,TITLE=My Document)']
    ... )

"""

import markdown
from markdown.util import etree

DEFAULT_URL = "http://packages.python.org/Markdown/"
DEFAULT_CREATOR = "laomo"
DEFAULT_TITLE = "Markdown To OPML"


class OPMLExtension (markdown.Extension):

    def extendMarkdown(self, md, md_globals):

        self.config = { 'URL' : [DEFAULT_URL, "Main URL"],
                        'CREATOR' : [DEFAULT_CREATOR, "Feed creator's name"],
                        'TITLE' : [DEFAULT_TITLE, "Feed title"] }

        md.xml_mode = True

        # Insert a tree-processor that would actually add the title tag
        treeprocessor = OPMLTreeProcessor(md)
        treeprocessor.ext = self
        md.treeprocessors['opml'] = treeprocessor
        md.stripTopLevelTags = 0
        md.docType = '<?xml version="1.0" encoding="utf-8"?>\n'


class OPMLTreeProcessor(markdown.treeprocessors.Treeprocessor):

    def run(self, root):

        opml = etree.Element("opml")
        opml.set("version", "2.0")

        header = etree.SubElement(opml, "header")
        title = etree.SubElement(header, "title")
        title.text = self.ext.getConfig("TITLE")

        body = etree.SubElement(opml, "body")

        groupoutline=None

        for child in root:
            if child.tag in ["h1", "h2", "h3", "h4", "h5"]:
                groupoutline = etree.SubElement(body, "outline")
                groupoutline.set("title", child.text.strip())
                groupoutline.set("text", child.text.strip())
            elif child.tag == "p":
                for item in child:
                    if item.tag == "a":
                        if groupoutline:
                            outline = etree.SubElement(groupoutline, "outline")
                        else:
                            outline = etree.SubElement(body, "outline")
                        outline.set("type", "rss")
                        outline.set("title", item.text.strip())
                        outline.set("xmlUrl", item.attrib['href'])
                        outline.set("htmlUrl", item.attrib['title'])

        return opml


def makeExtension(*configs):
    return OPMLExtension(*configs)
