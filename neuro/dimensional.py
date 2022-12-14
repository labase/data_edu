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

.. versionadded::    22.12a1
        adiciona classe Dimensional @1
"""
import json
from csv import writer
from csv import reader
from time import sleep
from html3 import HTML
import bs4 as bs
RATE = 4
HTTP = "http://"
SUB_DIMENSION = 0

BD, BM, BT, BL, DG, GG, LG, HB, DB, MB, BB, LB, CC = ("0066cc 44cddd 66c6cc 93cddd 4f6228 77933c c3d69b 984807 e46c0a"
                                                      " f09646 ff9666 fac090 cccccc").split()


class Dimension:
    def __init__(self, document=None, html_=None, csv="PRE-CRIVO.csv", page=""):
        self.document, self.html = document, html_
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

    def page(self, sub=1, alone=False):
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
        # from browser import ajax

        def read(req):
            print(req)
        print("vai", self.url)
        read(0)  # fake

        # ajax.get(self.url, oncomplete=read)


class Dimensional:
    def __init__(self, name_=("modelo dimensional:5:5",), tag="FILO", color="white", sup=None):
        self.name = name_
        # self.cs, self.rs = name.split(":")[1], name.split(":")[2]
        self.tag, self.sup, self.color = tag, sup, color
        self.sub_dimensions = []
        self.sub_tags = []
        self.hsub_tags = [[]for _ in range(60)]
        self.h_row = 0
        self.h = HTML()
        self.casa = {}
        self.h_themes = {}
        self.page_data = {}
        self.tag_matrix = [[] for _ in range(30)]
        self.header = ['ONTOGÊNESE', 'HABILIDADES DE ALFABETIZAÇÃO', 'ORALIDADE',
                       'Consciência fonêmica', 'Segmenta os fonemas']

        self.__htag = self.h.table(border="1", cellpadding="0", cellspacing="0", dir="ltr").thead()

    def page(self, sub=SUB_DIMENSION, alone=False, pager=HTML(), hd="Linguagem"):
        def refer(elt, url, tit, abt):
            elt.a(tit, href=f"{HTTP}{url}")
            elt.p(abt)

        def item(iid, elt):
            elt.a("", id=iid)
            title = self.casa[iid]
            elt.h2(title)
            if title in self.page_data:
                entries = self.page_data[title]
                [refer(elt, **entry) for entry in entries]
            elt.h2("Resumo")
            elt.p("Lorem Ipsum")

        head = f"Filogênese-Escrita-Microgênese-{hd}"
        dv = pager
        if alone:
            ht = HTML()
            ht.title(head)
            ht = ht.body()
            dv = ht.div()
        dv.h1(head)
        themes = self.tag_matrix[0]
        for line in themes:
            item(line, dv)
        return dv

    def get_tags(self, inx, iny):
        # print('get_tags', inx, iny, self.hsub_tags[iny], self.sub_tags[0:5])
        return "".join([tag[inx] for tag in self.sub_tags[0:5]]) + "".join([str(tg) for tg in self.hsub_tags[iny]])

    def htag(self):
        return self.__htag

    def __repr__(self):
        _ = [sub.go(self.__htag) for sub in self.sub_dimensions]
        return str(self.h)

    def create_v_sub(self, name_=("modelo dimensional",), tag="FILO", color="white"):
        class DimensionV(Dimensional):
            def __init__(self, _name=name_, _tag=tag, _color=color, sup=self):
                super().__init__(name_, tag, color, sup)

            # def __repr__(self):
            def go(self, tg):
                t = tg.tr
                # col_sp = len(self.name)//self.cs
                tags = []
                for namer in self.name:
                    # print(namer, namer.split(":"))
                    namer_, cs, rs, tg = namer.split(":")
                    t = t.th(scope="col", colspan=f'{cs}', rowspan=f'{rs}', bgcolor=color)
                    t.p(f"{namer_} ({tg})", style="text-align: center;")
                    tags += [tg]*int(cs)
                self.sup.sub_tags += [tags]
                self.sup.h_themes = {code.split(":")[-1]: code.split(":")[0] for code in self.name}
                return str(t)
        sub_dimension = DimensionV()
        self.sub_dimensions.append(sub_dimension)  # _name=name, _tag=tag, _color=color, sup=self))
        return sub_dimension

    def create_vh_sub(self, name=("modelo dimensional",), tag="FILO", color="white"):
        class DimensionVH(Dimensional):
            def __init__(self, _name=name, _tag=tag, _color=color, sup=self):
                super().__init__(name, tag, color, sup)

            def go(self, tg):
                t = tg.tr
                name_, cs, rs, tg = self.name.split(":")
                t = t.th(scope="row", colspan=f'{cs}', rowspan=f'{rs}', bgcolor=color)
                t.b.big.big.big.p(f"{name_} ({tg})", style="text-align: center;")
                # t.h1(f"{name_} ({tg})")
                return str(t)
        sub_dimension = DimensionVH()
        self.sub_dimensions.append(sub_dimension)  # _name=name, _tag=tag, _color=color, sup=self))
        return sub_dimension

    def create_h_sub(self, name_=("modelo dimensional",), tag="FILO", color=0):
        class DimensionH(Dimensional):
            def __init__(self, _name=name_, _tag=tag, _color=color, sup=self):
                super().__init__(name_, tag, "white", sup)
                self.cross = []
                fila = 5 - len(self.name)
                # self.colors = [HB, DB, BB, MB, LB, LB, LB][color:]
                self.colors = [HB, DB, BB, MB, LB, LB, LB][fila:]
                self.h_row = self.sup.h_row
                # self.colors.pop(color)

            def go(self, tg):
                t = tg.tr
                last_theme_name = []
                for namer in self.name:
                    cl = self.colors.pop(0)
                    # print(namer, namer.split(":"))
                    namer_, cs, rs, tg = namer.split(":")
                    n, nc, nr = f"{namer_} ({tg})", f'{cs}', f'{rs}'
                    t = t.th(n, scope="row", colspan=nc, rowspan=nr, bgcolor=cl) if cs != '0' else t
                    # self.sup.hsub_tags += [[tg] * int(rs)]
                    h_row = self.h_row
                    _ = [cts.append(tg) for cts in self.sup.hsub_tags[h_row:h_row+int(rs)]]
                    last_theme_name += ([namer_]+[" "]*(int(cs)-1))
                    # bk = 1 if int(cs) > 1 else bk
                bk = len(last_theme_name)
                self.sup.header = header = self.sup.header[:-bk]+last_theme_name

                # print("v, h", len(self.sup.sub_tags[0]), len(self.sup.hsub_tags[0]))
                for inx in range(19):
                    t = t.td(bgcolor=CC)
                    tag_name = self.sup.get_tags(inx, self.h_row)
                    t.small.small.small.a(tag_name, href=f"#{tag_name}")
                    self.sup.casa[tag_name] = f"{self.sup.h_themes[self.sup.sub_tags[-1][inx]]} — {'—'.join(header)}"
                    self.sup.tag_matrix[inx].append(tag_name)
                # print(self.sup.hsub_tags)
                # print(self.sup.get_tags(0, 0))

                return str(t)
        sub_dimension = DimensionH()
        self.sub_dimensions.append(sub_dimension)  # _name=name, _tag=tag, _color=color, sup=self))
        self.h_row += 1
        return sub_dimension


def html_read_table():
    def parse(td_, _, __):
        colspan = td_["colspan"] if 'colspan' in td_.attrs else '1'
        rowspan = td_["rowspan"] if 'rowspan' in td_.attrs else '1'
        text = td_.text.replace('\n', '')
        text, ttag = text.split(' (') if ' (' in text else (text, text[:3].upper())
        return ":".join([text, colspan, rowspan, ttag[:-1]])
    tabela_matriz = []
    with open('var/modelo.html', 'r') as table_file:
        table_raw = table_file.read()
        table = bs.BeautifulSoup(table_raw, "lxml")
        find_table = table.find('table', class_="modelo")
        rows = find_table.find_all('tr')
        # print(len(rows), rows[0], table_raw[:300])
        # tabela_matriz = [[parse(td, ix) for ix, td in enumerate(i.find_all('td')) if td.text != u'\xa0']for i in rows]
        for iy, ic in enumerate(rows):
            row = []
            for ix, td in enumerate(ic.find_all('td')):
                if td.text != u'\xa0':
                    row.append(parse(td, ix, iy))
            tabela_matriz.append(row) if row else None
        # tabela_matriz = [row + [" :1:1:_"] * (5-len(row)) if len(row) < 5 else row for row in tabela_matriz]
        # [print(row) for row in tabela_matriz[-30:]]
        return tabela_matriz


def htm3_write_from_reader():
    d = Dimensional()
    table = html_read_table()
    d.create_vh_sub("Ontogênese/Filogênese:5:6:OF", "F", "995599")
    _ = [print(",".join(row)) for row in table[:2]]
    head = zip(table, [BD, BM, DG, GG, LG])
    _ = [d.create_v_sub(row, "F", color) for row, color in head]
    _ = [d.create_h_sub(row, "F", 0) for row in table[5:]]
    print(d)
    # print(d.casa)
    # print(d.h_themes)
    print(d.page())


def htm3_write():
    d = Dimensional()
    d.create_vh_sub("Ontogênese/Filogênese:5:6:OF", "F", "995599")
    d.create_v_sub(["Filogênese:10:1:F"], "F", BD)
    d.create_v_sub(["Escrita:10:1:E"], "E", BM)
    d.create_v_sub(["Microgênese:10:1:M"], "M", DG)
    d.create_v_sub(["Função Cognitiva:10:1:FC"], "FC", GG)
    lin = ("Linguagem:1:1:L,Memória:1:1:M,Atenção:1:1:A,Percepção:1:1:P,Emoção:1:1:E,Lógica:1:1:O,Imaginário:1:1:I,"
           "Transitividade:1:1:T,Raciocínio:1:1:R,Representação:1:1:S")
    d.create_v_sub(lin.split(","), "FC", LG)
    lin = ("ONTOGÊNESE:1:9:O,HABILIDADES DE ALFABETIZAÇÃO:1:9:HA,ORALIDADE:1:5:OR,"
           "Consciência fonêmica:1:3:CF,Segmenta os fonemas:1:1:SF")
    d.create_h_sub(lin.split(","), "FC", 0)
    lin = "Gestos fonoarticulatórios:1:1:GF"
    d.create_h_sub(lin.split(","), "FC", 4)
    lin = "Ouve e Lembra:1:1:OL"
    d.create_h_sub(lin.split(","), "FC", 4)
    lin = "Expressão Oral:1:3:EO,Express Interações:1:1:EE"
    d.create_h_sub(lin.split(","), "FC", 3)
    print(d)


def splinter_new_page():
    # require: pip install splinter[selenium3]
    from splinter import Browser
    from ltk import AUT
    from selenium import webdriver
    from uuid import uuid4
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    caps['acceptInsecureCerts'] = True
    # browser = Browser('firefox')  # , headless=True)cr
    # browser = Browser('chrome', options={"acceptInsecureCerts": True})  # , headless=True)
    browser = Browser('chrome', desired_capabilities=caps)  # , headless=True)
    # return
    browser.visit('https://activufrj.nce.ufrj.br/')
    browser.find_by_name('user').fill(AUT['user'])
    browser.find_by_name('passwd').fill(AUT['passwd'])
    browser.find_by_css('button').first.click()
    cookies = browser.cookies.all()
    print(cookies)

    if browser.is_text_present('Carlo Emmanoel Tolla de Oliveira'):
        print("Yes, the official website was found!")
    else:
        print("No, it wasn't found... We need to improve our SEO techniques")
    page_name = f'Splinter_page_{str(uuid4())[-4:]}'
    browser.visit('https://activufrj.nce.ufrj.br/wiki/newpage/carlo?folder=5db0e33e9f4a4b6bb91c381032ac300d')
    browser.find_by_name('nomepag').fill(page_name)
    with browser.get_iframe(0) as iframe:
        conteudo = f'<p>página criada : {str(uuid4())}</p></br>'
        iframe.find_by_css('body.cke_editable').type(conteudo)
    browser.find_by_id("cke_16").first.click()
    browser.find_by_name('nomepag').fill(page_name)
    browser.find_by_text('Enviar').first.click()
    if browser.is_text_present(conteudo):
        print("Yes, conteudo was found!")
        browser.visit(f'https://activufrj.nce.ufrj.br/wiki/edit/carlo/{page_name}')
        browser.find_by_text('Enviar').first.click()
    browser.quit()


def main(document, html_):
    cfile = "http://localhost:8000/PRE-CRIVO.csv"
    cpage = "http://localhost:8000/var/Memoria.json"
    Dimension(document, html_, cfile, cpage).vai()


def ducker(coluna=4):
    dm = Dimension()

    print(dm.raw_csv[5])
    [print(dm.casa[key[coluna]]) for key in dm.raw_csv[6:16]]
    query_list_ = [dm.casa[key[coluna]] for key in dm.raw_csv[6:16]]
    duck = Duck("Memória", file="Memoria")
    duck.pager(query_list=query_list_)
    duck.save()
    # Duck('Memória Linguagem').vai('Memória Linguagem')


if __name__ == '__main__':
    # splinter_new_page()
    # htm3_write()
    # html_read_table()
    htm3_write_from_reader()
    # ducker()
