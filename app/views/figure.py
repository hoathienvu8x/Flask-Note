# -*- coding: utf-8 -*-

import re
from markdown import Extension
from markdown.util import etree
from markdown.inlinepatterns import IMAGE_LINK_RE
from markdown.treeprocessors import Treeprocessor
from markdown.inlinepatterns import LinkInlineProcessor
from markdown.extensions.attr_list import AttrListTreeprocessor

class ImageInlineProcessor(LinkInlineProcessor):

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        if not handled:
            return None, None, None

        src, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        fig = etree.Element('figure')
        img = etree.SubElement(fig, 'img')
        img.set('src', 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=')

        img.set('data-src', src)

        if title is not None:
            img.set("title", self.unescape(title))

        if '::cap::' in text:
            alt, caption = [ v.strip() for v in text.split("::cap::")]
            if caption:
                cap = etree.SubElement(fig, 'figcaption')
                cap.text = caption

            img.set('alt', self.unescape(alt))
        else:
            img.set('alt', self.unescape(text))

        if 'attr_list' in self.md.treeprocessors:
            curly = re.match(AttrListTreeprocessor.BASE_RE, data[index:])
            if curly:
                fig[-1].tail = '\n'
                fig[-1].tail += curly.group()
                index += curly.endpos

        return fig, m.start(0), index

class FigureTreeprocessor(Treeprocessor):
    def run(self, root):
        for p in root.iterfind('p'):
            figure = p.find("figure")
            if figure is not None:
                p.tag = None
                p.attrib = None

class FigureCaption(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.register(ImageInlineProcessor(IMAGE_LINK_RE, md), 'caption', 151)
        md.treeprocessors.register(FigureTreeprocessor(md), 'fig_cap', 7)
