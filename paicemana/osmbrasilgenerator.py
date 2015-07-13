import json, urllib
import requests, wget, feedparser  # TODO in setup.py
from pprint import pprint  # TODO in setup.py

class Week(object):

    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.__set_number__()
    
    def __set_number__(self):
        self.number = self.title.split()[1]
    
    def __str__(self):
        return self.title


class JSONDownload(object):  # TODO class's comment
    """Class to ..."""

    def __init__(self):

        self.weeks = []

        url = 'http://pipes.yahoo.com/pipes/pipe.run?_id=1062c25a278564badfe33e04382d40a8&_render=json'
        response = requests.get(url)
        data = response.json()
        
        for item in data['value']['items']:
            w = Week(item['title'], item['link'])
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


class RSSDownload(object):  # TODO class's comment DON'T USE IT
    """Class to ..."""
  
    def __init__(self, url='http://pipes.yahoo.com/pipes/pipe.run?_id=6a998c98efa04e57b9a6babadcfc462b&_render=rss', filename='weeklyosm-pt.xml'):
        self.__filename = filename        
        urllib.request.urlretrieve (url, self.__filename)

    def __str__(self):
        return self.__filename


class RSSDownloadMinimal(RSSDownload):  # TODO class's comment DON'T USE IT
    
    def __init__(self, url='http://pipes.yahoo.com/pipes/pipe.run?_id=1062c25a278564badfe33e04382d40a8&_render=rss', filename='weeklyosm-pt.min.xml'):
        return super(RSSDownloadMinimal, self).__init__(url, filename) 


# https://validator.w3.org/feed/

class RSSDownloadFromScratch(object):  # TODO class's comment # TODO
    """Class to ..."""

    def __init__(self):

        url = 'http://www.weeklyosm.eu/pt/feed'
        self.feed = feedparser.parse(url)


if __name__ == "__main__":
    #print(JSONDownload())
    print(JSONDownload().markdown())
    #pprint(RSSDownloadFromScratch().feed)
    #print(RSSDownload())
    #print(RSSDownloadMinimal())
