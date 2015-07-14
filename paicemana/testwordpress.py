import re

lang = 'Ja'
text = 'My text here'

src="""<!--:en-->weekly 256 - 09.06.–15.06.2015<!--:-->

<!--:es-->semanario 256 - 09.06.–15.06.2015<!--:--><!--:Ja-->週刊OSM 256 - 09.06.–15.06.2015<!--:--><!--:fr-->hebdo 256 - 09.06.–15.06.2015<!--:--><!--:cz-->týdeník 256 - 
09.06.–\r
15.06.2015<!--:--><!--:id-->edisi minggu 256 - 09.06.–15.06.2015<!--:--><!--:tr--> 256 - 09.06.–15.06.2015<!--:--><!--:pt-->semanário 256 - 09.06.–15.06.2015<!--:-->
<!--:de-->Wochennotiz 256 - 09.06.–15.06.2015<!--:--><!--:ro-->Săptămânal nr. 256 - 09.06.–15.06.2015<!--:-->
"""

from testwordpresscontent import src

# to negate a word 'bar': '^(?!.*?bar).*' or '^(.(?<!bar))*?$'

out = re.sub(
    r'^(.*)(<!--:%s-->)(.(?<!<\!--:-->))*?(<!--:-->)(.*)$' % lang,
    r'\1\2%s\4\5' % text,
    src,
    flags = re.MULTILINE + re.DOTALL
)

print()
print(src)
print()
print(out)
print()
