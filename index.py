#!/usr/bin/python
#-*-coding: utf-8 -*-

from flask import Flask, request, render_template, send_from_directory
import os
import sys
import markdown
import urllib
import xml.dom.minidom
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding("utf-8")


app = Flask(__name__)
app.config.from_pyfile('config.cfg')


@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        try:
            mytype = request.form['type']
            if mytype == '1':
                url = request.form['url']
                if "http" not in url:
                    url = "http://" + url
                md = unicode(urllib.urlopen(url).read(), 'utf-8')
            elif mytype == '2':
                content = request.form['content']
                print content
                md = unicode(content, 'utf-8')
                md = "content"
                print md
            text = markdown.markdown(md, ['opml'])
            # text_xml = xml.dom.minidom.parse(xml_fname)
            text_xml = xml.dom.minidom.parseString(text)
            text = text_xml.toprettyxml(encoding='utf-8')
            if 'outline' in text:
                result = text
            else:
                print 'is not a markdown file !'
        except:
                print 'url is not a markdown file !'
    return render_template('index.html', result=result, active=0)


@app.route('/about')
def about():
    return render_template('about.html', active=1)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
