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
"""
from csv import reader
BD, BL, DG, GG, LG, HB, DB, BB, LB, CC = "0066cc 93cddd 4f6228 77933c c3d69b 984807 e46c0a f79646 fac090 cccccc".split()


class Dimension:
    def __init__(self, document=None, html=None, csv="/home/carlo/Downloads/PRE-CRIVO.csv"):
        self.document, self.html = document, html
        self.table = self.document["pydiv"]
        self.raw_csv = []
        self.casa = {}
        with open(csv, 'r') as file:
            _reader = reader(file)
            for each_row in _reader:
                self.raw_csv.append(each_row)
                print(each_row)

    def vai(self):
        w, r, d, h = self.html, self.html.TR, self.html.TD, self.html.TH
        spn = len(self.raw_csv[5])
        cartesians = [DB, BB, LB] + (spn-3)*[CC]
        self.casa = {line[0]: line[1] for line in self.raw_csv if line[0].startswith("FEM")}
        # print(self.casa)
        self.table.html = ""
        _ = self.table <= (tb := w.TABLE())
        _ = tb <= r(h("FILO", colspan=spn, bgcolor=BD))
        _ = tb <= r(h("Escrita", colspan=spn, bgcolor=BL))
        # _ = tb <= r("Escrita", bgcolor=BL)
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

    def page(self, sub=1, alone=False):
        def item(iid, elt):
            a = w.A(Id=iid)
            _ = a <= w.H2(self.casa[iid])
            _ = elt <= a
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
        # with open(f"var/{hfile}", 'w') as file:
        #     file.write(ht.html)
        return dv


class Duck:
    def __init__(self, query):
        from urllib.parse import quote_plus, quote
        link_params = {'q': query, 'format': "json"}
        # self.url = f"https://api.duckduckgo.com/?t=ffab&q={quote_plus(query)}&format=json&ia=web"
        # self.url = f"https://api.duckduckgo.com/html/?q={quote_plus(query)}"
        self.url = f"https://api.duckduckgo.com/html/?q={quote(query)}&format=json"
        print(self.url)

    def vai(self):
        import urllib.request
        fp = urllib.request.urlopen(self.url)
        mybytes = fp.read()

        mystr = mybytes.decode("utf8")
        fp.close()

        # print(mystr)
        self.parse(mystr)

    def parse(self, data):
        from bs4 import BeautifulSoup

        parsed = BeautifulSoup(data, features="lxml")
        # topics = parsed.findAll('div', {'id': 'zero_click_topics'})[0]
        # topics = parsed.findAll('div', {'id': 'links'})[0]
        # results = topics.findAll('div', {'class': re.compile('results_*')})
        # results = topics.findAll('div', {'class': 'results_snippet'})
        # results = parsed.findAll('div', {'class': 'result_snippet'})
        titles = parsed.findAll('a', {'class': 'result__a'})
        results = parsed.findAll('a', {'class': 'result__snippet'})

        [print(f"[{title.text[:20]}]", result.text[:250]) for title, result in zip(titles, results)]

    def vai_(self):
        from browser import ajax

        def read(req):
            print(req)
        print("vai", self.url)

        ajax.get(self.url, oncomplete=read)


def main(document, html):
    cfile = "http://localhost:8000/PRE-CRIVO.csv"
    Dimension(document, html, cfile).vai()


if __name__ == '__main__':
    # Duck("Memória e Produção Escrita").vai()
    Duck('Memória Linguagem').vai()
