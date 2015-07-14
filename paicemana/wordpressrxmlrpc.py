from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts

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
