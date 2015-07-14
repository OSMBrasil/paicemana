from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts

import re


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


if __name__ == "__main__":
    #test()
    post = MockPost()
    #print(post)
    changer = ChangerPosting(post)
    s = 'My text here'
    changer.do_for(s, s)
    changer.print_test()

