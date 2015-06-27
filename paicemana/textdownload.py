import urllib.request
import html2text
import re

from lxml import html
from lxml import etree

class MarkdownDownload(object):
    """Class to download text weeklyosm.eu"""

    def __init__(self, archive):
        """
        @params
        archive - number in permalink like www.weeklyosm.eu/archives/4205
        """

        self.url = 'http://www.weeklyosm.eu/archives/%s' % archive
        self.page = html.fromstring(urllib.request.urlopen(self.url).read())

        root = self.page.xpath('//article')[0]
        etree.strip_tags(root,'div','span')
        root_html = etree.tostring(root, pretty_print=True)

        markdown = html2text.html2text(root_html.decode('utf-8'))

        s = markdown
        s = re.sub(r'\n *', '\n', s)
        s = re.sub(r'^ *', '', s)
        s = re.sub(r'\n', '\n\n', s)
        s = re.sub(r'\n\n\n\n?', '\n\n', s)
        s = re.sub(r'…', '...', s)
        s = s.split('### Share this:')[0]
        markdown = s
        #print(markdown)

        self.filename = 'archive-%s.md' % archive
        self.markdown = markdown

        with open(self.filename, 'w') as text_file:
            text_file.write(markdown)

