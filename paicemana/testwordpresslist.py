"""
10/27/2015-11/2/2015

[caption id="attachment_12684" align="aligncenter" width="807"]<a href="http://blog.openstreetmap.de/wp-uploads//2015/11/before-after-road-styles-2.jpg"><img class=" wp-image-12684" src="http://blog.openstreetmap.de/wp-uploads//2015/11/before-after-road-styles-2.jpg" alt="neuer Carto Map Style auf osm.org" width="807" height="606" /></a> New OSM Carto Map Style at osm.org <a href="#wn276_maps">[1]</a> Data: OpenStreetMap-Contributors, Image CC-BY-SA 2.0 <a href="http://www.openstreetmap.org/">OpenStreetMap.org</a>[/caption]
<h2 id="wn276_mapping">Mapping</h2>
<ul>
...
http://blog.openstreetmap.de/wp-uploads//2015/11/before-after-road-styles-2.jpg
http://blog.openstreetmap.de/wp-uploads//2015/11/before-after-road-styles-2.jpg
"""

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts


def test_pages(user, password):
    client = Client('http://www.weeklyosm.eu/xmlrpc.php', user, password)
    results = client.call(posts.GetPosts())
    p = results[0]
    print(p.id)
    #print(p.title)


if __name__ == "__main__":
    test_pages('alexandre', 'SENHA')

# Getting all posts is broken

"""
alexandre@notebook-itautec paicemana $ python paicemana/testwordpresslist.py
Traceback (most recent call last):
  File "paicemana/testwordpresslist.py", line 56, in <module>
    test_pages('alexandre', '*******')
  File "paicemana/testwordpresslist.py", line 49, in test_pages
    results = client.call(posts.GetPosts())
  File "/usr/lib/python3.5/site-packages/python_wordpress_xmlrpc-2.3-py3.5.egg/wordpress_xmlrpc/base.py", line 37, in call
  File "/usr/lib/python3.5/xmlrpc/client.py", line 1091, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python3.5/xmlrpc/client.py", line 1431, in __request
    verbose=self.__verbose
  File "/usr/lib/python3.5/xmlrpc/client.py", line 1133, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python3.5/xmlrpc/client.py", line 1149, in single_request
    return self.parse_response(resp)
  File "paicemana/testwordpresslist.py", line 39, in parse_response
    p.feed(data)
  File "/usr/lib/python3.5/xmlrpc/client.py", line 438, in feed
    self._parser.Parse(data, 0)
xml.parsers.expat.ExpatError: not well-formed (invalid token): line 1010, column 196
"""

# http://www.scriptscoop.com/t/59768a9a3cf4/xml-rpc-python-client-raising-xml-parsers-expat-expaterror-exception.html

# http://www.sourcecodebrowser.com/python3.2/3.2.3~rc1/classxmlrpc_1_1client_1_1_transport.html
