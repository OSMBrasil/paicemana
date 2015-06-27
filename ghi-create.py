#!/usr/bin/python
#
# ATENÇÃO! AVISO DE IMPORTÂNCIA MÁXIMA:    NÃO EXECUTE ESTE SCRIPT
#
# O código está demasiadamente imaturo, apesar de já fazer o essencial do que
# se espera dele: popula o repositório OSMBrasil/semanario com issues.
#
# A EXECUÇÃO DESTE CÓDIGO PODE ENCHER O REPOSITÓRIO DE ISSUES INDESEJADAS.
#
# Este programa está sendo compartilhado em tal estado apenas como forma de
# transmitir conhecimento e atestar os marcos alcançados. Como proponente de
# um fluxo de trabalho sofisticado para OSMBrasil/semanario, usando kanban,
# e que está em pleno ensaio, preciso deixar visíveis os progressos.
#
# Na maturidade este programa estará integrado como comando do paicemana.
#
# @ alexandre-mbm ‒ Alexandre Magno ‒ alexandre.mbm@gmail.com 

milestone = 1               # 256 (1), 257 (2)
label = 'revisão'           # tradução, revisão, movimento, conserto
filename = 'revisoes.csv'   # traducoes.csv, revisoes.csv

repo_user = 'OSMBrasil'
repo_name = 'semanario'

from github3 import login, GitHub

cards = [
    { 'section': 'Events', 'translator': 'jgpacker'},
    { 'section': 'Humanitarian OSM', 'translator': 'jgpacker'},
    { 'section': 'Maps', 'translator': 'jgpacker'},
    { 'section': 'Software', 'translator': 'jgpacker'},
    { 'section': 'Did you know...', 'translator': 'jgpacker'},
    { 'section': 'Other "geo" things', 'translator': 'vgeorge'}
]

cards = []

import csv
with open(filename, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter='|')
    for row in spamreader:
        cards.append(row)

#exit(0)

from getpass import getpass, getuser
import sys
try:
    import readline
except ImportError:
    pass

# Fix Python 2.x. see: http://stackoverflow.com/a/7321970/3391915
try:
    input = raw_input
except NameError:
    pass

try:
    user = input('GitHub username: ')
except KeyboardInterrupt:
    user = getuser()

password = getpass('GitHub password for {0}: '.format(user))

# Obviously you could also prompt for an OAuth token
if not (user and password):
    print("Cowardly refusing to login without a username and password.")
    sys.exit(1)

github = login(user, password)

repo = github.repository(repo_user, repo_name)

for card in cards:
    repo.create_issue(
        card['section'],
        body=None,
        assignee=card['translator'],
        milestone=milestone,
        labels=[label]
    )
