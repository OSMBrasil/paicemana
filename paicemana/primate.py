import webbrowser
import sys

"""
paicemana sync      # baixa as listas de ids do OSMBC e do Wordpress, atualizando dados locais

paicemana check     # lista os últimos semanários possíveis e valida estado de coisas

paicemana get 277   # baixa HTML do OSMBC, e informações do Wordpress
                    # consulta estado do artigo e da imagem, nos sistemas e nas configurações

paicemana put       # joga documento para o Wordpress (instruções)
                    # apaga o arquivo localmente

paicemana restore   # restaura arquivos de controle com os padrões do pacote instalado
"""

class BrowserAction(object):

    FILENAME = 'FILENAME'
    URL = None

    def __init__(self):
        self.filename = self.FILENAME
        self.url = self.URL

    def do(self):
        print('Remember save it as "%s".\n' % self.filename)
        print('Press ENTER to continue and open the browser...')
        print(' or CTRL+C to exit.')
        try:
            input()
            webbrowser.open_new_tab(self.url)
        except KeyboardInterrupt:
            sys.exit(0)
        print()
        print('  WARNING !!! TAKE CARE !!!!!!\n')
        print('  We hope you have saved "%s" correctly!\n' % self.filename)
        print('  Try "paicemana check" before of another actions.\n')


class GetContentOSMBC(BrowserAction):

    FILENAME = '/tmp/weekly.htm'
    URL = 'https://thefive.sabic.uberspace.de/blog/%s/preview?download=true&lang=%s'

    def __init__(self, blogid=307, lang='PT'):
        super(GetContentOSMBC, self).__init__()
        self.url = self.URL % (str(blogid),lang)


class PageAction(BrowserAction):

    def do(self):
        print('You need save a web page as HTML file only.')
        super(PageAction, self).do()


class GetListOSMBC(PageAction):

    FILENAME = '/tmp/osmbc.htm'
    URL = 'https://thefive.sabic.uberspace.de/blog/list'


class GetListWordpress(PageAction):

    FILENAME = '/tmp/wordpress.htm'
    URL = 'http://www.weeklyosm.eu/wp-admin/edit.php'


def previous_tests():

    #GetContentOSMBC(306).do()

    print(GetContentOSMBC.FILENAME)
    print(GetContentOSMBC().filename)
    print(GetContentOSMBC.URL)
    print(GetContentOSMBC().url)

    print(GetListOSMBC.FILENAME)
    print(GetListOSMBC().filename)
    print(GetListOSMBC.URL)
    print(GetListOSMBC().url)


if __name__ == "__main__":

    #GetContentOSMBC().do()
    #GetListOSMBC().do()
    GetListWordpress().do()

