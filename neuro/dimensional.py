#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Neuro22
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL-3 <https://bit.ly/gpl_v3>`__.
# SPDX-License-Identifier: (GPL-3.0-or-later AND LGPL-2.0-only) WITH bison-exception
"""Gerador de modelo dimensional em HTML.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.12a0
        primeira versão @05
        com resultados das pesquisas @07
"""
import json
from csv import writer
from csv import reader
from time import sleep
RATE = 4
HTTP = "http://"

BD, BL, DG, GG, LG, HB, DB, BB, LB, CC = "0066cc 93cddd 4f6228 77933c c3d69b 984807 e46c0a f79646 fac090 cccccc".split()


class Dimension:
    def __init__(self, document=None, html=None, csv="PRE-CRIVO.csv", page=""):
        self.document, self.html = document, html
        self.table = None
        self.raw_csv = []
        self.casa = {}
        with open(csv, 'r') as file:
            _reader = reader(file)
            for each_row in _reader:
                self.raw_csv.append(each_row)
                # print(each_row)
        self.casa = {line[0]: line[1] for line in self.raw_csv if line[0].startswith("FEM")}
        if not page:
            return
        with open(page, 'r') as file:
            self.page_data = json.load(fp=file)
            print(self.page_data.keys())

    def vai(self):
        self.table = self.document["pydiv"]
        w, r, d, h = self.html, self.html.TR, self.html.TD, self.html.TH
        spn = len(self.raw_csv[5])
        cartesians = [DB, BB, LB] + (spn-3)*[CC]
        # print(self.casa)
        self.table.html = ""
        _ = self.table <= (tb := w.TABLE())
        _ = tb <= r(h("FILO", colspan=spn, bgcolor=BD))
        _ = tb <= r(h("Escrita", colspan=spn, bgcolor=BL))
        r0 = r()
        _ = [r0 <= (h(cl, bgcolor=DG, colspan=spn-3) if cl != " " else d(cl)) for cl in " , , ,Micro".split(",")]
        _ = tb <= r0
        r0 = r()
        _ = [r0 <= (d(cl, bgcolor=HB, colspan=3) if (ct < 1) else d(cl, bgcolor=LG))
             for ct, cl in enumerate(self.raw_csv[5]) if cl]
        _ = tb <= r0
        cnt = range(spn)
        row_span = [[1]*spn for _ in range(10)]
        row_clip = [2]*10
        row_clip[0] = 0
        row_clip[3] = 1
        row_clip[5] = 1
        row_span[0][0] = 10
        row_span[0][1] = 3
        row_span[3][0] = 2
        row_span[5][0] = 5
        for lc, line in enumerate(self.raw_csv[6:16]):
            r0 = r()
            _ = [r0 <= d(
                w.A(cl, href=f"#{cl}") if "FEM" in cl else cl, Id=f"md{lc}_{ct}", bgcolor=cc, rowspan=row_span[lc][ct])
                 for ct, cc, cl in zip(cnt, cartesians[row_clip[lc]:], line[row_clip[lc]:])]
            _ = tb <= r0
        self.document["md0_0"].rowspan = 10
        _ = self.table <= self.page()

    def page(self, sub=0, alone=False):
        def refer(elt, url, tit, abt):
            _ = elt <= w.A(tit, href=f"{HTTP}{url}")
            _ = elt <= w.P(abt)

        def item(iid, elt):
            a = w.A(Id=iid)
            title = self.casa[iid]
            _ = a <= w.H2(title)
            _ = elt <= a
            if title in self.page_data:
                entries = self.page_data[title]
                [refer(elt, **entry) for entry in entries]
            else:
                _ = elt <= w.P("Lorem Ipsum")

        w = self.html
        hd = self.raw_csv[5][sub+3].split(' (')[0]
        head = f"Filogênese-Escrita-{hd}"
        dv = w.DIV()
        if alone:
            ht = w.HTML()
            _ = ht <= w.TITLE(head)
            bd = w.BODY()
            _ = ht <= bd
            _ = bd <= dv
        _ = dv <= w.H1(head)
        for lc, line in enumerate(self.raw_csv[6:16]):
            item(line[sub+3], dv)
        return dv


class Duck:
    def __init__(self, query, file="test", fold="var/"):
        self.query, self.file, self.fold = query, file, fold
        self.file = f'{self.fold}{self.file.replace(" ", "_")}.json'

        self.result = []
        self.page = {}
        self.url = "https://duckduckgo.com/html/?q={}&format=json"
        # self.url = "https://api.duckduckgo.com/html/?q={}&format=json"
        print(self.url)

    def pager(self, query_list):
        def do_query(query):
            self.vai(query=query)
            sleep(RATE)
        [do_query(query) for query in query_list]

    def vai(self, query):
        from urllib.parse import quote
        import urllib.request
        self.query = query
        url = self.url.format(quote(query))
        print("vai: ", url)
        with urllib.request.urlopen(url) as response:
            html_result = response.read()

            html_result = html_result.decode("utf8")
            # print(html_result)
            self.parse(html_result)

    def parse(self, data):
        from bs4 import BeautifulSoup
        resulted = []

        parsed = BeautifulSoup(data, features="lxml")
        titles = parsed.findAll('a', {'class': 'result__a'})
        results = parsed.findAll('a', {'class': 'result__snippet'})
        links = parsed.findAll('a', {'class': 'result__url'})
        filename = f'{self.fold}{self.file.replace(" ", "_")}.json'
        # filename = f'{self.fold}{self.query.replace(" ", "_")}.csv'
        print(filename)

        [resulted.append(dict(url=f"{link.text.strip()}", tit=f"{title.text}", abt=result.text))
         for link, title, result in zip(links, titles, results)]
        # [print(f"[{link.text.strip()[:100]}]", f"[{title.text[:20]}]", result.text[:250])
        #  for link, title, result in zip(links, titles, results)]
        self.page[self.query] = resulted
        print(resulted)

    def save(self, csv="", data=None):
        import json
        csv = csv or self.file
        data = data or self.page
        with open(csv, 'w+', newline='') as file:
            json.dump(data, file)

    def save_(self, csv, data=None):
        data = data or self.result
        with open(csv, 'w+', newline='') as file:
            _writer = writer(file, delimiter='|', quotechar='"', dialect='unix')
            _writer.writerows(data)

    def vai_(self):
        from browser import ajax

        def read(req):
            print(req)
        print("vai", self.url)

        ajax.get(self.url, oncomplete=read)


def spl():
    # require: pip install splinter[selenium3]
    from splinter import Browser
    from ltk import AUT

    browser = Browser('firefox', headless=True)
    browser.visit('https://activufrj.nce.ufrj.br/')
    browser.find_by_name('user').fill(AUT['user'])
    browser.find_by_name('passwd').fill(AUT['passwd'])
    browser.find_by_css('button').first.click()
    cookies = browser.cookies.all()
    print(cookies)
    # browser.find_by_name('btnK')

    if browser.is_text_present('Carlo Emmanoel Tolla de Oliveira'):
        print("Yes, the official website was found!")
    else:
        print("No, it wasn't found... We need to improve our SEO techniques")

    browser.quit()


def main(document, html):
    cfile = "http://localhost:8000/PRE-CRIVO.csv"
    cpage = "http://localhost:8000/var/Linguagens.json"
    Dimension(document, html, cfile, cpage).vai()


def ducker(coluna = 4):
    dm = Dimension()

    print(dm.raw_csv[5])
    [print(dm.casa[key[coluna]]) for key in dm.raw_csv[6:16]]
    query_list_ = [dm.casa[key[coluna]] for key in dm.raw_csv[6:16]]
    duck = Duck("Memória", file="Memoria")
    duck.pager(query_list=query_list_)
    duck.save()
    # Duck('Memória Linguagem').vai('Memória Linguagem')


if __name__ == '__main__':
    spl()
