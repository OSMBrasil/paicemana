import webbrowser


class Paiabridor(object):

    def __init__(self, repo_user='OSMBrasil', repo_name='semanario'):
        tmpl_github = 'https://www.github.com/%s/%s'
        tmpl_waffle = 'https://waffle.io/%s/%s'
        self.url_github = tmpl_github % (repo_user, repo_name)
        self.url_waffle = tmpl_waffle % (repo_user, repo_name)

    def issues(self, milestone=None):
        if not milestone:
            # https://github.com/OSMBrasil/semanario/issues
            url = self.url_github + '/issues'
            webbrowser.open_new_tab(url)
        else:
            # https://github.com/OSMBrasil/semanario/issues?q=is%3Aopen+is%3Aissue+milestone%3A256
            url = self.url_github + '/issues?q=is%3Aopen+is%3Aissue+milestone%3A' + str(milestone)
            webbrowser.open_new_tab(url)

    def translation(self, edition, branch='master', suffix='semanario'):  # -n/--open INTEGER
        #https://github.com/OSMBrasil/semanario/blob/master/256-semanario.md
        tmpl = self.url_github + '/blob/%s/%s-%s.md'
        url = tmpl % (branch, edition, suffix)
        webbrowser.open_new_tab(url)

    def commits(self, branch='master'):
        #https://github.com/OSMBrasil/semanario/commits/master
        tmpl = self.url_github + '/commits/%s'
        url = tmpl % branch
        webbrowser.open_new_tab(url)

    def diff(self, point1='HEAD%5E1', point2='master'):  # TODO encode params
        #https://github.com/OSMBrasil/semanario/compare/HEAD%5E1...master
        tmpl = self.url_github + '/compare/%s...%s'
        url = tmpl % (point1, point2)
        webbrowser.open_new_tab(url)
    
    def project(self):
        webbrowser.open_new_tab(self.url_github)

    def kanban(self, milestone=None, user=None):
        if not milestone and not user:
            # https://waffle.io/OSMBrasil/semanario
            webbrowser.open_new_tab(self.url_waffle)
        elif milestone and not user:
            # https://waffle.io/OSMBrasil/semanario?milestone=256
            tmpl = self.url_waffle + '?milestone=%s'
            url = tmpl % milestone
            webbrowser.open_new_tab(url)
        elif not milestone and user:
            # https://waffle.io/OSMBrasil/semanario?assigned=alexandre-mbm
            tmpl = self.url_waffle + '?assigned=%s'
            url = tmpl % user
            webbrowser.open_new_tab(url)
        else:
            # https://waffle.io/OSMBrasil/semanario?milestone=256&assigned=alexandre-mbm
            tmpl = self.url_waffle + '?milestone=%s&assigned=%s'
            url = tmpl % (milestone, user)
            webbrowser.open_new_tab(url)


"""
-i/--issues [INTEGER] para abrir página de issues [de milestone] no navegador
-n/--open INTEGER para abrir o arquivo no navegador (HTML do GitHub)
-c/--commits para abrir página de commits no navegador
-d/--diff para abrir página de diff no navegador
-p/--project para abrir página inicial do projeto no navegador
-k/--kanban [INTEGER] [-u/--user STRING] para abrir kanban no waffle.io
"""

if __name__ == "__main__":
    nav = Paiabridor()
    #nav.project()
    #nav.kanban()
    #nav.kanban(256)
    #nav.kanban(user='alexandre-mbm')
    #nav.kanban(256,'alexandre-mbm')
    #nav.commits()
    #nav.commits('vgeorge')    
    #nav.issues()
    #nav.issues(256)
    #nav.translation(256)
    nav.diff()
