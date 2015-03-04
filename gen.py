#!/usr/bin/python
#-*-coding: utf-8 -*-
import markdown
import codecs
import sys
import urllib
import xml.dom.minidom
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding("utf-8")


if len(sys.argv) > 1:
    try:
        md = urllib.urlopen(sys.argv[1]).read()
        md = unicode(md, 'utf-8')
        print markdown.markdown(md)
    except:
        print 'url is not a markdown file !'
else:
    input_file = codecs.open("podcasts.md", mode="r", encoding="utf8")
    md = input_file.read()

text = markdown.markdown(md, ['opml'])
if text == '<opml version="2.0"><header><title>Markdown To OPML</title></header><body></body></opml>':
    print 'is not a markdown file !'
if 'outline' not in text:
    print 'is not a markdown file !'

#text_xml = xml.dom.minidom.parse(xml_fname)
text_xml = xml.dom.minidom.parseString(text)
text = text_xml.toprettyxml(encoding='utf-8')
print text
