import re

lang = 'Ja'
text = 'My text here'

from testwordpresscontent import src_title as src

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
