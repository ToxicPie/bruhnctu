import markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re


class SpoilerPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        elem = etree.Element('span')
        elem.set('class', 'spoiler')
        elem.set('tabindex', '-1')
        elem.set('title', 'You\'ve known too much.')
        elem.text = m.group(3)
        return elem

class UnderlinePattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        elem = etree.Element('span')
        elem.set('class', 'underline')
        elem.text = m.group(3)
        return elem

class InlineMathPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        elem = etree.Element('span')
        elem.set('class', 'math-container')
        elem.text = m.group(2)
        return elem

class DisplayMathPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        elem = etree.Element('div')
        elem.set('class', 'math-container')
        elem.text = m.group(2)
        return elem

# stolen from https://github.com/Python-Markdown/markdown/blob/master/markdown/extensions/admonition.py
class AlertProcessor(BlockProcessor):
    CLASSNAME = 'alert'
    CLASSNAME_TITLE = 'alert-title'
    RE = re.compile(r'(?:^|\n)!!! ?([\w\-]+(?: +[\w\-]+)*)(?: +"(.*?)")? *(?:\n|$)')
    RE_SPACES = re.compile('  +')

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        return self.RE.search(block) or \
            (block.startswith(' ' * self.tab_length) and sibling is not None and
             sibling.get('class', '').find(self.CLASSNAME) != -1)

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        m = self.RE.search(block)

        if m:
            block = block[m.end():]  # removes the first line

        block, theRest = self.detab(block)

        if m:
            klass, title = self.get_class_and_title(m)
            div = etree.SubElement(parent, 'div')
            div.set('class', '{} {}'.format(self.CLASSNAME, klass))
            if title:
                p = etree.SubElement(div, 'p')
                p.text = title
                p.set('class', self.CLASSNAME_TITLE)
        else:
            div = sibling

        self.parser.parseChunk(div, block)

        if theRest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, theRest)

    def get_class_and_title(self, match):
        klass, title = match.group(1).lower(), match.group(2)
        klass = self.RE_SPACES.sub(' ', klass)
        if title is None:
            # no title was provided, use the capitalized classname as title
            # e.g.: `!!! note` will render
            # `<p class="admonition-title">Note</p>`
            title = klass.split(' ', 1)[0].capitalize()
        elif title == '':
            # an explicit blank title should not be rendered
            # e.g.: `!!! warning ""` will *not* render `p` with a title
            title = None
        return klass, title

DEL_RE = r'(~~)(.*?)~~'
SPO_RE = r'(\|\|)(.*?)\|\|'
UND_RE = r'(__)(.*?)__'
SLA_RE = r'(\/\/)(.*?)\/\/'
MATH_RES = [
    # r'((\$+)(.+?)\$+)',
    r'((\$\$)(.+?)\$\$)',
    r'((\\\\\[)(.+?)\\\\\])',
    # r'((\$)(.+?)\$)',
    r'[^\$]((\$)([^\$]+?)\$)',
    r'((\\\\\()(.+?)\\\\\))'
]
# MATH_RE_ALL = r'((\\\[)(.*?)\\\])|((\$\$)(.*?)\$\$)|((\$)(.*?)\$)|((\\\()(.*?)\\\))'

class MyExtension(Extension):
    def extendMarkdown(self, md, *args):
        del_pattern = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.register(del_pattern, 'del', 105)
        spo_pattern = SpoilerPattern(SPO_RE)
        md.inlinePatterns.register(spo_pattern, 'spoiler', 105)
        und_pattern = UnderlinePattern(UND_RE)
        md.inlinePatterns.register(und_pattern, 'underline', 105)
        # math patterns
        # priority 185, 186: lower than `` and higher than most things
        # display math is higher
        math_pattern = DisplayMathPattern(MATH_RES[0])
        md.inlinePatterns.register(math_pattern, 'math_0', 186)
        math_pattern = DisplayMathPattern(MATH_RES[1])
        md.inlinePatterns.register(math_pattern, 'math_1', 186)
        math_pattern = InlineMathPattern(MATH_RES[2])
        md.inlinePatterns.register(math_pattern, 'math_2', 185)
        math_pattern = InlineMathPattern(MATH_RES[3])
        md.inlinePatterns.register(math_pattern, 'math_3', 185)

        md.parser.blockprocessors.register(AlertProcessor(md.parser), 'alert', 200)

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
