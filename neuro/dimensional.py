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
            _ = [r0 <= d(cl, Id=f"md{lc}_{ct}", bgcolor=cc, rowspan=row_span[lc][ct])
                 for ct, cc, cl in zip(cnt, cartesians[row_clip[lc]:], line[row_clip[lc]:])]
            _ = tb <= r0
        self.document["md0_0"].rowspan = 10


def main(document, html):
    cfile = "http://localhost:8000/PRE-CRIVO.csv"
    Dimension(document, html, cfile).vai()


if __name__ == '__main__':
    Dimension()
