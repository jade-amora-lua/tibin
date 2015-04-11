#!/usr/bin/python3

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

DEFAULT_ARGS = ("2015",
                "10/04",
                "10/04",
                "null",
                "1,1000,1010,1020,2,2000,3,3000,3020,4000,5000,6000,126,4,5,6,20,21,",
                "",
                "1",
                "pesquisa_avancada",
                "exteriores")

class ImprensaNacional(object):

    def __init__(self, ano, fim, inicio,
               fonetica, jornal, jornal_hidden,
               paginaAtual, tipoPesquisa, txtPesquisa):
        self.url = "http://pesquisa.in.gov.br/imprensa/core/consulta.action"
        self.search_params = [
            ("edicao.ano", ano),
            ("edicao.dtFim", fim),
            ("edicao.dtInicio", inicio),
            ("edicao.fonetica", fonetica),
            ("edicao.jornal", jornal),
            ("edicao.jornal_hidden", jornal_hidden),
            ("edicao.paginaAtual", paginaAtual),
            ("edicao.tipoPesquisa", tipoPesquisa),
            ("edicao.txtPesquisa", txtPesquisa)]

    def search(self):
        postdata = urllib.parse.urlencode(self.search_params).encode('ascii')
        pageread = urllib.request.urlopen(self.url, postdata).read()
        page = pageread.decode("utf-8")
        soup = BeautifulSoup(page[-5000:])
        paginacao = soup.find(id="paginacao")
        # First substring of paginacao:
        results_description = next(paginacao.span.strings)

        # First word of results:
        word = results_description.split()[0]

        if word == "Nenhum":
            self.numberofresults = 0
        else:
            try:
                self.numberofresults = int(word)
            except:
                print("Error converting number of results: %s" % word)

imprensa = ImprensaNacional(*DEFAULT_ARGS)

imprensa.search()
print(imprensa.numberofresults)

# This is how an empty page looks
# <div id="paginacao">
# <span>Nenhum item encontrado para a pesquisa solicitada.</span><br>
# </div>

# And this have results:
# <div id="paginacao">
# <span>8 itens encontrados, exibindo 1 a 10. [<b>Primeiro</b>/<b>Anterior</b>]
# &nbsp;<b>1</b>&nbsp;&nbsp;[<b>Próximo</b>/<b>Último</b>]
# </div>
