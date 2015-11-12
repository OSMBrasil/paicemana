from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts, media

import re
import sys
import html2text

from human import CorrelationJSON, ImageCode


def test():

    client = Client(
                        'http://www.weeklyosm.eu/xmlrpc.php',
                        'alexandre', 'SENHA'
                    )

    posts = client.call(posts.GetPosts())

    #for post in posts[:1]:
        #print(posts[1].id)
        #print(posts[1].title)
        #print(posts[1].link)
    print(posts[0].content)

    # http://python-wordpress-xmlrpc.readthedocs.org/en/latest
    #
    # http://codex.wordpress.org/XML-RPC_WordPress_API
    # https://github.com/maxcutler/python-wordpress-xmlrpc/


class MockPost(object):

    def __init__(self):
        from testwordpresscontent import src_title as title
        from testwordpresscontent import src_content as content
        self.title = title
        self.content = content

    def __str__(self):
        return '\n%s\n\n%s\n' % (self.title, self.content)


class ChangerPosting(object):

    def __init__(self, post, lang='Ja'):
        self.post = post
        self.lang = lang

    def do(src, text, lang):
        return re.sub(
            r'^(.*)(<!--:%s-->)(.(?<!<\!--:-->))*?(<!--:-->)(.*)$' % lang,
            r'\1\2%s\4\5' % text,
            src,
            flags = re.MULTILINE + re.DOTALL
        )

    def do_for(self, newTitle=None, newContent=None):
        if newTitle:
            self.post.title = ChangerPosting.do(
                                                    self.post.title,
                                                    newTitle,
                                                    self.lang
                                               )
        if newContent:
            self.post.content = ChangerPosting.do(
                                                    self.post.content,
                                                    newContent,
                                                    self.lang
                                                 )

    def print_test(self):
        print(self.post)


class ExtractorPosting(object):

    def __init__(self, post, lang='Ja'):
        self.post = post
        self.lang = lang

    def do(src, lang):
        return re.findall(
            r'<!--:%s-->((.(?<!<\!--:-->))*)' % lang,
            src,
            flags = re.MULTILINE + re.DOTALL
        )[0][0][:-7]

    def do_content(self):
        return ExtractorPosting.do(self.post.content, self.lang)

    def do_title(self):
        return ExtractorPosting.do(self.post.title, self.lang)


# TODO a class MarkdownDownload() here, using the ExtractorPosting()

class MarkdownDownload(object):
    """Class to download text weeklyosm.eu"""

    def __init__(self, user, password, archive, sync=False):
        """
        @params
        archive - number in permalink like www.weeklyosm.eu/archives/4205
        sync - True for downloading the brazilian version already published
        """

        client = Client('http://www.weeklyosm.eu/xmlrpc.php', user, password)
        self.post = client.call(posts.GetPost(archive))

        lang = 'en' if not sync else 'pt'
        extractor = ExtractorPosting(self.post, lang)
        content = extractor.do_content()
        markdown = html2text.html2text(content)

        s = markdown
        s = re.sub(r'^ *\*', '*', s, flags = re.MULTILINE)
        s = re.sub(r'([^\n]\n)\*', r'\1\n*', s, flags = re.MULTILINE)
        s = re.sub(r'…', '...', s)
        s = re.sub(r'“', '"', s)
        s = re.sub(r'”', '"', s)
        markdown = s
        #print(markdown)
        """
        caption = re.findall(
            r'\[caption.*caption\]',
            markdown,
            flags = re.MULTILINE + re.DOTALL
        )[0]  # TODO bug with 4639

        out = re.sub(r'\n', ' ', caption)
        out = re.sub(r'(\(http[^\)]*) ', r'\1', out)

        markdown = markdown.replace(caption, out)
        """
        self.filename = 'archive-%s.md' % archive
        self.markdown = markdown

        with open(self.filename, 'w') as text_file:
            text_file.write(markdown)


class Migrate_pt2pb(object):

    def __init__(self, user, password, archive, lfrom='pt', lto='pb'):
        client = Client('http://www.weeklyosm.eu/xmlrpc.php', user, password)
        post = client.call(posts.GetPost(archive))
        tagfrom = '[:%s]' % lfrom
        tagto = '[:%s]' % lto
        post.title = post.title.replace(tagfrom, tagto)
        post.content = post.content.replace(tagfrom, tagto)
        #print(post.title)
        #print(post.content)
        client.call(posts.EditPost(post.id, post))

class FixJaponese(object):

    def __init__(self, user, password, archive):
        client = Client('http://www.weeklyosm.eu/xmlrpc.php', user, password)
        post = client.call(posts.GetPost(archive))
        tag1_from = '<!--:Ja-->'
        tag2_from = '[:Ja]'
        tag1_to = '<!--:ja-->'
        tag2_to = '[:ja]'
        post.title = post.title.replace(tag1_from, tag1_to)
        post.title = post.title.replace(tag2_from, tag2_to)
        post.content = post.content.replace(tag1_from, tag1_to)
        post.content = post.content.replace(tag2_from, tag2_to)
        client.call(posts.EditPost(post.id, post))

def test_pages(user, password):
    from wordpress_xmlrpc import WordPressPage
    client = Client('http://www.weeklyosm.eu/xmlrpc.php', user, password)
    pages = client.call(posts.GetPosts({'post_type': 'page'}, results_class=WordPressPage))
    p = pages[0]
    print(p.id)
    print(p.title)

def test_get_post(user, password, archive):
    client = Client('http://www.weeklyosm.eu/xmlrpc.php', user, password)
    post = client.call(posts.GetPost(archive))
    print(post.title)

def test_a():
    #test()
    post = MockPost()
    #print(post)
    """
    changer = ChangerPosting(post)
    s = 'My text here'
    changer.do_for(s, s)
    changer.print_test()
    """
    extractor = ExtractorPosting(post, 'pt')
    print(extractor.do_title())
    print(extractor.do_content())


class PuppetOfMedia(object):

    def __init__(self, user, password):
        self.client = Client('http://www.weeklyosm.eu/xmlrpc.php', user, password)

    def getList(self, parent=0, limit=5):
        d = { 'number': limit, 'parent_id': parent }
        return self.client.call(media.GetMediaLibrary(d))

    def getItem(self, id=5782):
        return self.client.call(media.GetMediaItem(id))

    def getItemFor(self, week):
        myjson = CorrelationJSON()  # TODO do singleton?
        myjson.load()
        myjson.non_multiples()
        parent = myjson.get_wordpress_id_for(276)
        return self.getList(parent, limit=1)[0]  # TODO is it unique? looks forever?


def print_small(collection, with_link=False):
    if with_link:
        print()
    for media in collection:
        print(media.id, '|', media.parent, '|', media.title)
        if with_link:
            print(media.link)
            print()

def create_image_code(media_item, lang='pb'):
    return ImageCode(
        id = media_item.id,
        width = media_item.metadata['width'],
        height = media_item.metadata['height'],
        url = media_item.link,
        alt = media.title,  # TODO fix it to use "lang"
        text = media.caption,  # TODO fix it to use "lang"
        anchor = None
    )


if __name__ == "__main__":

    puppet = PuppetOfMedia('alexandre', 'SENHA')

    media = puppet.getItem()
    #print(create_image_code(media))
    print(media.title)

    exit(0)

    print(media.id)
    print(media.parent)
    print(media.link)
    print(media.metadata)
    print(media.title)
    print(media.caption)
    print(media.description)

    exit(0)

    print_small([puppet.getItemFor(276)], with_link=True)

    exit(0)

    print_small(puppet.getList())

    exit(0)

    print_small(puppet.getList(parent=5742), True)

    exit(0)

    #test_a()
    #MarkdownDownload('alexandre', 'SENHA', 4391, True)
    #Migrate_pt2pb('alexandre', 'SENHA', 4639)
    #test_pages('alexandre', 'SENHA')
    #test_get_post('alexandre', 'SENHA', 3353)
    FixJaponese('alexandre', 'SENHA', int(sys.argv[1]))

