import urllib.request
import html2text
import re

from lxml import html
from lxml import etree

class MarkdownDownload(object):
    """Class to download text weeklyosm.eu"""

    def __init__(self, archive, sync=False):
        """
        @params
        archive - number in permalink like www.weeklyosm.eu/archives/4205
        sync - True for downloading the brazilian version already published
        """

        lang = 'en' if not sync else 'pt'
        self.url = 'http://www.weeklyosm.eu/%s/archives/%s' % (lang, archive)
        self.page = html.fromstring(urllib.request.urlopen(self.url).read())

        root = self.page.xpath('//article')[0]
        etree.strip_tags(root,'div','span')
        root_html = etree.tostring(root, encoding='utf-8', pretty_print=True, method='html')

        markdown = html2text.html2text(root_html.decode('utf-8'))

        s = markdown
        s = re.sub(r'\n *', '\n', s)
        s = re.sub(r'^ *', '', s)
        s = re.sub(r'\n', '\n\n', s)
        s = re.sub(r'\n\n\n\n?', '\n\n', s)
        s = re.sub(r'…', '...', s)
        s = re.sub(r'“', '"', s)
        s = re.sub(r'”', '"', s)
        s = re.sub(r' \[\]\(.*\/OSMBrasil\/semanario.*\n\n.*\)', '', s)
        s = s.split('### Share this:')[0]
        s = s.split('### Compartilhe isso:')[0]
        s = re.sub(r'## *', '## ', s)
        markdown = s
        #print(markdown)

        self.filename = 'archive-%s.md' % archive
        self.markdown = markdown

        with open(self.filename, 'w') as text_file:
            text_file.write(markdown)

