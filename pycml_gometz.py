#!/usr/bin/python
# -*- coding: utf-8 -*-
# $Id: pycml_gometz.py 124 2008-12-17 10:49:51Z almacha $

# I, River Champeimont, the author of this work,
# hereby release it into the public domain.
# This applies worldwide.
# 
# In case this is not legally possible:
# I grant anyone the right to use this work for any purpose,
# without any conditions, unless such conditions are required by law.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# This program requires Python >= 2.5.

import xml.etree.ElementTree as ET
import cgi

def escape(s):
    return cgi.escape(s, quote = True)

def put_string_in_file(filename, str):
    f = open(filename, 'wb')
    f.write(str.encode("UTF-8"))
    f.close()

def make_xhtml_begin(title):
    return u"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html 
     PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<link rel="stylesheet" title="Default pycml_gometz style" href="../webdata/style.css"/>
<title>%s</title>
</head>
<body>
""" % escape(title)

def make_xhtml_end():
    return u"""<p class="publicdomain">Les photos et le programme qui a servi a générer cette page sont dans le domaine public. Vous pouvez <a href="https://github.com/rchampeimont/pycml_gometz">consulter le code source du programme</a>.</p>\n""" \
    + ("""<pre>%s</pre>\n""" % u"""$Id: pycml_gometz.py 124 2008-12-17 10:49:51Z almacha $""") \
    + """</body>
</html>
"""

directions = ('down', 'left', 'forward', 'right', 'up')
dirtexts = {'down':'bas',
            'left':'gauche',
            'forward':'avancer',
            'right':'droite',
            'up':'haut'}

def make(city):
    r"""city is the directory name"""

    tree = ET.parse('%s/index.xml' % city)
    root = tree.getroot()
    settings = root.find('settings')
    resolution = settings.find('resolution')
    width = resolution.get('width')
    if width == 'auto':
        width = None
    else:
        width = int(width)
    startplaces = settings.find('startplaces')
    img_style = ""
    if width:
         img_style += ' style="width: %dpx;"' % width

    def make_xhtml_index(startplaces):
        s = make_xhtml_begin(escape(city))
        s += '<h1>%s</h1>\n' % escape(city)
        s += '<ul>\n'
        for startplace in startplaces.findall('start'):
            s += """<li><a href="%s">%s</a></li>\n""" % \
                  (escape("%s.xhtml" % startplace.get('first')),
                  escape(startplace.get('title')))
        s += '</ul>\n'
        s += make_xhtml_end()
        put_string_in_file('%s/index.xhtml' % city, s)

    def make_xhtml_place(img):
        def dirtext(dir):
            x = img.get(dir)
            if x:
                return (("""<a href="%s.xhtml" title="%s">""" % (x, x))
                        + dirtexts[dir] + """</a>""")
            else:
                return ''

        s = make_xhtml_begin(escape("%s - %s" % (city, img.get('id'))))
        s += """<table style="width: 100%;">\n<tr>\n"""
        for dir in ('down', 'left', 'forward', 'right', 'up'):
            s += """<td class="directions" style="width: 20%%;">%s</td>\n""" % \
                dirtext(dir)
        s += """</tr>\n</table>\n"""
        s += """<p style="text-align: center;"><img src="%s" alt="%s" title="%s"%s/></p>\n""" % (img.get('src'), img.get('id'), img.get('id'), img_style)
        s += make_xhtml_end()
        put_string_in_file('%s/%s.xhtml' % (city, img.get('id')), s)



    print "Making index..."
    make_xhtml_index(startplaces)
    
    body = root.find('body')
    for img in body.findall('img'):
        print 'Making %s...' % img.get('id')
        make_xhtml_place(img)
        

def makeall():
    cities = ['gometz']
    for city in cities:
        make(city)


makeall()
