from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagPattern

DEL_RE = r'(~~)(.*?)~~'
SPO_RE = r'(\|\|)(.*?)\|\|'
INS_RE = r'(__)(.*?)__'
STRONG_RE = r'(\*\*)(.*?)\*\*'
EMPH_RE = r'(\/\/)(.*?)\/\/'

class MyExtension(Extension):
    def extendMarkdown(self, md, *args):
        del_tag = SimpleTagPattern(DEL_RE, 'del')
        md.inlinePatterns.add('del', del_tag, '>not_strong')
        spo_tag = SimpleTagPattern(SPO_RE, 'spoiler')
        md.inlinePatterns.register(spo_tag, 'spoiler', 60)
        md.inlinePatterns.add('spo', spo_tag, '>spoiler')
        # ins_tag = SimpleTagPattern(INS_RE, 'ins')
        # md.inlinePatterns.add('ins', ins_tag, '>del')
        # strong_tag = SimpleTagPattern(STRONG_RE, 'strong')
        # md.inlinePatterns['em_strong'] = strong_tag
        # emph_tag = SimpleTagPattern(EMPH_RE, 'em')
        # md.inlinePatterns['emphasis'] = emph_tag
        # md.inlinePatterns.deregister('em_strong2')

def makeExtension(**kwargs):
    return MyExtension(**kwargs)
