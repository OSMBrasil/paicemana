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
#     @alexandre-mbm  ‒  Alexandre Magno  ‒  alexandre.mbm@gmail.com
#
############################   Variables   #####################################

translators = ['alexandre-mbm', 'jgpacker', 'vgeorge']

milestone = 1               # 256 (1), 257 (2)

label_t = 'tradução'        # tradução, revisão, movimento, conserto
label_r = 'revisão'         # tradução, revisão, movimento, conserto

filename = 'archive-4205.md'

repo_user = 'OSMBrasil'
repo_name = 'semanario'

#############################   Preload   ######################################

from paicemana.mdanalyzer import MarkdownAnalyzer
from getpass import getpass, getuser
from github3 import login, GitHub

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

#############################   Functions   ####################################

def get_github():

    try:
        user = input('GitHub username: ')
    except KeyboardInterrupt:
        user = getuser()

    password = getpass('GitHub password for {0}: '.format(user))

    # Obviously you could also prompt for an OAuth token
    if not (user and password):
        print("Cowardly refusing to login without a username and password.")
        sys.exit(1)

    return login(user, password)

def put_issues_of_translations(organizer):  # TODO use or change
    for section in organizer.sections:
        repo.create_issue(
            section.name,
            body=None,
            assignee=section.translator,
            milestone=milestone,
            labels=[label_t]
        )

def put_issues_of_revisions(organizer):  # TODO use or change
    for section in organizer.sections:
        repo.create_issue(
            section.name,
            body=None,
            assignee=section.reviser,
            milestone=milestone,
            labels=[label_r]
        )

def test_print_sections(organizer):
    for section in organizer.sections:
        print(section.score, section.translator, section.reviser, section.name)

def test_put_issues_of_translations(organizer):
    print(milestone, label_t)

def test_put_issues_of_revisions(organizer):
    print(milestone, label_r)

#############################   Program   ######################################

if __name__ == "__main__":

    analyzer = MarkdownAnalyzer(filename)
    organizer = analyzer.getOrganizer()
    organizer.distribute_for(translators)

    github = get_github()

    repo = github.repository(repo_user, repo_name)

    test_print_sections(organizer)
    test_put_issues_of_translations(organizer)
    test_put_issues_of_revisions(organizer)

