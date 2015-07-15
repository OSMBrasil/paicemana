import re


src = """23.06.‒29.06.2015

[caption id="attachment_11897" align="alignnone" width="640"]![Doações num
gráfico em barras, uma coluna por dia](http://www.weeklyosm.eu/wp-
content/uploads/2015/07/258-chart.svg) Doações durante a campanha de
angariação de fundos para o financiamento de um novo hardware para o
OpenStreetMap. [Gráfico: Nakaner; Dados: Frederik
Ramm.](https://lists.openstreetmap.org/pipermail/osmf-
talk/attachments/20150630/feede3ff/attachment-0001.png) [1][/caption]

## Sobre nós

* O time WeeklyOSM saúda seus novos amigos [brasileiros](http://www.weeklyosm.eu/pt/) ![Português do Brasil](http://blog.openstreetmap.de/wp-uploads//2015/01/pt-br.svg) [Vitor, Alexandre e João](https://wiki.openstreetmap.org/wiki/WeeklyOSM#Languages). Sejam bem vindos, “Welcome”, caríssimos amigos do país da [capoeira](https://en.wikipedia.org/wiki/Capoeira), da praia de [Copacabana](https://en.wikipedia.org/wiki/Copacabana_\\\(Rio_de_Janeiro\\)), da [caipirinha](https://en.wikipedia.org/wiki/Caipirinha), de [Jorge Amado](https://en.wikipedia.org/wiki/Jorge_Amado) e [Oscar Niemeyer](https://en.wikipedia.org/wiki/Oscar_Niemeyer)! ;)

* Durante julho e agosto o WeeklyOSM tirará umas pequenas férias de verão. Será fornecido um resumo mensal no início de agosto e outro no início de setembro.

## Mapeamento"""


out = re.findall(
    r'\[caption.*caption\]',
    src,
    flags = re.MULTILINE + re.DOTALL
)[0]

out = re.sub(r'\n', ' ', out)
out = re.sub(r'(\(http[^\)]*) ', r'\1', out)

print(out)
