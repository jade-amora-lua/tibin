#!/usr/bin/python3

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

search_param = [
    ("edicao.ano", "2015"),
    ("edicao.dtFim", "10/04"),
    ("edicao.dtInicio", "10/04"),
    ("edicao.fonetica", "null") ,
    ("edicao.jornal",
     "1,1000,1010,1020,2,2000,3,3000,3020,4000,5000,6000,126,4,5,6,20,21,"),
    ( "edicao.jornal_hidden", ""),
    ("edicao.paginaAtual", "1"),
    ("edicao.tipoPesquisa", "pesquisa_avancada"),
    ("edicao.txtPesquisa", "saboga")]

url = "http://pesquisa.in.gov.br/imprensa/core/consulta.action"

postdata = urllib.parse.urlencode(search_param).encode('ascii')

# retrieve file-like object with search results
page = urllib.request.urlopen(url, postdata)

# special methodos of the urllib-generated object

# has the link been redirected?
# new_url = page.geturl()

# what meta information did we receive?
meta = page.info()

pageread = page.read()

page = pageread.decode("utf-8")

with open("/tmp/dou-astext-003.txt", 'w') as astextwrite:
    astextwrite.write(page)


# ugly hack: the page we received is composed of two html trees, so we
# grab only the last 1000 bytes
soup = BeautifulSoup(page[-1000:])

paginacao = soup.find(id="paginacao")

# First substring of paginacao:
results_description = next(paginacao.span.strings)

# First word of results:
word = results_description.split()[0]

if word == "Nenhum":
    numberofresults = 0
else:
    try:
        numberofresults = int(word)
    except:
        print("Error converting number of results: %s" % word)

print("Número de resultados: %d" % numberofresults)

# This is how an empty page looks
# <div id="paginacao">
# <span>Nenhum item encontrado para a pesquisa solicitada.</span><br>
# </div>

# And this have results:
# <div id="paginacao">
# <span>8 itens encontrados, exibindo 1 a 10. [<b>Primeiro</b>/<b>Anterior</b>]
# &nbsp;<b>1</b>&nbsp;&nbsp;[<b>Próximo</b>/<b>Último</b>]
# </div>
