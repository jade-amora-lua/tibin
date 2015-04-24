#!/usr/bin/python3

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import argparse
import datetime
import sys
import subprocess
import os.path
import shutil
import re

DEFAULT_ARGS = {"ano": "2015",
                "fim": "13/04",
                "inicio": "10/04",
                "fonetica": "null",
                "jornal": "1,1000,1010,1020,2,2000,3,3000,3020,4000,5000,6000,126,4,5,6,20,21,",
                "jornal_hidden": "",
                "tipoPesquisa": "pesquisa_avancada",
                "txtPesquisa": "exteriores remover"}

class ImprensaNacional(object):

    def __init__(self, ano, fim, inicio,
                 fonetica, jornal, jornal_hidden,
                 tipoPesquisa, txtPesquisa):
        self.url = "http://pesquisa.in.gov.br/imprensa/core/consulta.action"
        # print(ano, fim, inicio, fonetica)
        self.search_params = {
            "edicao.ano":  ano,
            "edicao.dtFim":  fim,
            "edicao.dtInicio":  inicio,
            "edicao.fonetica":  fonetica,
            "edicao.jornal":  jornal,
            "edicao.jornal_hidden":  jornal_hidden,
            "edicao.paginaAtual":  "1",
            "edicao.tipoPesquisa":  tipoPesquisa,
            "edicao.txtPesquisa":  txtPesquisa}
        self.results = self.search()
        self.numberofresults = len(self.results)

    def processfirstpage(self, contents):
        paginacao = contents.find(id="paginacao")
        # First substring of paginacao:
        results_description = next(paginacao.span.strings)
        # First word of results:
        word = results_description.split()[0]
        if word == "Nenhum":
            # print(contents)
            numberofresults = 0
        else:
            try:
                numberofresults = int(word)
            except:
                print("Error converting number of results: %s" % word)
        return numberofresults


    def search(self):
        contents = self.getcontents(1)
        numberofresults = self.processfirstpage(contents)
        if numberofresults == 0:
            return []

        results = self.parseresults(contents)
        # print("Results - first page: %s." % results)
        numberofpages = (numberofresults-1)//10
        for page in range(1,numberofpages):
            pagecontents = self.getcontents(page)
            results.extend(self.parseresults(pagecontents))
        return(results)

    def getcontents(self, page=1):
        search_params = self.search_params
        search_params["edicao.paginaAtual"] = "%d" % page
        postdata = urllib.parse.urlencode(search_params).encode('ascii')
        pageread = urllib.request.urlopen(self.url, postdata).read()
        page = pageread.decode("utf-8")
        pagepart = page[page.index('html'):]
        soup = BeautifulSoup(pagepart)
        contents = soup.find(id="conteudo")
        # print(contents)
        return contents

    def parseresults(self, contents):
        """Parse results out of contents tree."""
        results = []
        targets = contents.findAll("th", class_="data")
        excerpts = contents.findAll("td", class_="data")
        for target, excerpt in zip(targets, excerpts):
            link = target.a["href"]
            link_description = target.getText()
            excerpt = excerpt.getText()
            results.append((link, link_description, excerpt))
        return(results)

    def getpdf(self, result):
        link, description, excerpt = result
        
        direction = link.split('?')[1]
        basepath = "http://pesquisa.in.gov.br/imprensa/servlet/INPDFViewer?"
        addendum = "&captchafield=firistAccess"
        fulllink = basepath + direction + addendum

        page = urllib.request.urlopen(fulllink)

        localpath = "/tmp"
        localname = slugify(description)
        localext = ".pdf"
        localfqn = os.path.join(localpath, localname + localext)

        if os.path.exists(localfqn):
            print("File exists. Aborting.")
        else:
            with open(localfqn, "bw") as writefile:
                shutil.copyfileobj(page, writefile)
        return localfqn


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    value = re.sub('[-\s]+', '-', value)
    return value


def getoptions():
    parser = argparse.ArgumentParser(description="Pesquisar no Diário Oficial.")
    parser.add_argument('--datainicio', '-i', metavar="dd/mm[/yyyy]",
                        help="Data inicial para busca.\nAtenção: o ano deve "
                        "ser o mesmo para o início e para o fim. Caso os dois "
                        "sejam definidos, será utilizado somente o do fim.")
    parser.add_argument('--datafim', '-f', metavar="dd/mm[/yyyy]",
                       help="Data final para busca.")
    parser.add_argument('busca', nargs='+',
                        help="Termos para busca.")
    parser.add_argument('--scripting', '-s', action="store_false",
                        help="Não entrar no modo interativo. Use esse modo para "
                        "usar a saída em outros programas.")
    return parser.parse_args()
    

def normalize_date(date):
    if not date:
        today = datetime.date.today()
        day, month, year = today.day, today.month, today.year
    else:
        datelist = date.split('/')
        if len(datelist) == 2:
            datelist.append(0)
        if len(datelist) == 3:
            try:
                day, month, year = [ int(x) for x in datelist ]
            except:
                print("Error converting date %s." % date)
                raise
    return ("%02d/%02d" % (day, month), "%4d" % year)
    
def main():
    opts = getoptions()

    inicio, anoinicio = normalize_date(opts.datainicio)
    DEFAULT_ARGS['inicio'] = inicio

    fim, anofim = normalize_date(opts.datafim)
    DEFAULT_ARGS['fim'] = fim

    if int(anofim):
        ano = anofim
    elif int(anoinicio):
        ano = anoinicio
    else:
        ano = "%4d" % datetime.date.today().year
    DEFAULT_ARGS['ano'] = ano
        
    if opts.busca:
        DEFAULT_ARGS['txtPesquisa'] = ' '.join(opts.busca)
        
    imprensa = ImprensaNacional(**DEFAULT_ARGS)

    messages = [ "Número de resultados: %d." % imprensa.numberofresults ]
    for i, (link, link_description, excerpt) in enumerate(imprensa.results):
        message = "Número: %d.\n" % i
        message += "Link: %s.\n" % link
        message += "Link description: %s.\n\n" % link_description
        message += "Excerpt: %s." % excerpt
        messages.append(message)
    print("\n===========\n".join(messages))

    if imprensa.numberofresults == 0:
        sys.exit(1)
    elif opts.scripting:
        while 1:
            print("Escolha um dos resultados para visualizar, ou enter para sair.")
            choice = input("> ")
            if choice == "":
                break
            else:
                choice = int(choice)
            filename = imprensa.getpdf(imprensa.results[choice])
            print("Abrindo arquivo %s." % filename)
            if sys.platform.startswith('linux'):
                subprocess.call(['xdg-open', filename])
            else:
                subprocess.call(['start', filename])

if __name__ == "__main__":
    main()
# This is how an empty page looks
# <div id="paginacao">
# <span>Nenhum item encontrado para a pesquisa solicitada.</span><br>
# </div>

# And this have results:
# <div id="paginacao">
# <span>8 itens encontrados, exibindo 1 a 10. [<b>Primeiro</b>/<b>Anterior</b>]
# &nbsp;<b>1</b>&nbsp;&nbsp;[<b>Próximo</b>/<b>Último</b>]
# </div>
