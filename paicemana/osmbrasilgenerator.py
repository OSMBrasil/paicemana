import json, datetime
import feedparser, PyRSS2Gen  # TODO in setup.py
from lxml import etree  # TODO in setup.py


class Week(object):

    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.__set_number__()
    
    def __set_number__(self):
        self.number = self.title.split()[1]
    
    def __str__(self):
        return self.title


class DataCaught(object):  # TODO class's comment
    """Class to ..."""

    def __init__(self):

        self.weeks = []

        url = 'weeklyosm.xml'
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            w = Week(entry.title, entry.link)
            self.weeks.append(w)

    def __str__(self):
        s = ''
        for w in self.weeks:
            s = '%s\n%s' % (s, w) if s else w
        return s

    def markdown(self):
        return self.__md_items__() + '\n\n' + self.__md_links__()

    def __md_items__(self):
        s = ''
        for w in self.weeks:
            s = '%s- [%s]%s\n' % (s, w.title, self.__md_label_for__(w.number))
        return s[:-1]

    def __md_links__(self):
        s = ''
        for w in self.weeks:
            s = '%s%s: %s\n' % (s, self.__md_label_for__(w.number), w.link)
        return s[:-1]

    def __md_label_for__(self, number):
        return '[weeklyosm-%s]' % number


# https://pythonhosted.org/DeeFuzzer/deefuzzer.deefuzzer.tools.PyRSS2Gen-module.html

class PaicemanaFeed(PyRSS2Gen.RSS2):

    rss_attrs = {
        "version": "2.0",
        "xmlns:atom": "http://www.w3.org/2005/Atom"
    }

    def __init__(self, selflink=None, *args, **kwargs):
        self.selflink = selflink
        super(PaicemanaFeed, self).__init__(*args, **kwargs)

    def publish_extensions(self, handler):

        if self.selflink:
            PyRSS2Gen._element(handler, 'atom:link', None,
                           {'rel': 'self',
                            'type': 'application/rss+xml',
                            'href': self.selflink,
                            })

        #def characters(self, key, description):
        #    self._out.write('%s<![CDATA[\n %s \n]]>%s' % ("<%s>"%key, description, "</%s>"%key))
        #characters(handler, "description", self.d1)


# https://validator.w3.org/feed/

class RSSDownload(object):  # TODO class's comment # TODO
    """Class to ..."""

    def __init__(self):

        url = 'http://www.weeklyosm.eu/pb/feed'
        self.feed = feedparser.parse(url)
        self.__filter__()
        self.__transform__()
        self.__write__()
        self.__format__()

    def __filter__(self):
        to_remove = []
        for entry in self.feed.entries:
            if not entry.title \
               or len(entry.title) == 0 \
               or entry.title.startswith('(English)'):
                to_remove.append(entry)
        for e in to_remove:
            self.feed.entries.remove(e)

    def __transform__(self):
        for entry in self.feed.entries:
            entry.title = entry.title.replace('.‒', ' a ')
            entry.title = entry.title.replace('.–', ' a ')
            entry.title = entry.title.replace('.-', ' a ')
            entry.title = entry.title.replace('.', '/')

    def __write__(self):
        rss = PaicemanaFeed(
            title = "WeeklyOSM em Português do Brasil",
            link = "http://www.openstreetmap.com.br/weeklyosm.xml",
            description = "Um resumo semanal de todas as coisas que acontecem no mundo do OpenStreetMap",
            lastBuildDate = datetime.datetime.now(),
            docs = None,
            image = PyRSS2Gen.Image(
                url = self.feed.feed.image.href,
                title = self.feed.feed.image.title,
                link = self.feed.feed.image.link,
                width=self.feed.feed.image.width,
                height=self.feed.feed.image.height
            ),
            selflink = "http://www.openstreetmap.com.br/weeklyosm.xml",
            items = self.__items_for_write__()
        )
        rss.write_xml(open("weeklyosm.xml", "w"), encoding = "utf-8")

    def __format__(self):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse("weeklyosm.xml", parser)
        tree.write("weeklyosm.xml", pretty_print=True)

    def __items_for_write__(self):
        items = []
        for entry in self.feed.entries:
            item =  PyRSS2Gen.RSSItem(
                title = entry.title,
                link = entry.link,
                description = None,
                guid = entry.id,
                pubDate = entry.published
            )
            items.append(item)
        return items


if __name__ == "__main__":
    RSSDownload()
    #print(DataCaught())
    print(DataCaught().markdown())

