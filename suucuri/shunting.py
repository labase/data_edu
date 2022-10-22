#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Manobrando o trem nos trilhos ABCD

O principal objetivo do jogo é formar um trem constituído de 5 dos 8 vagões
 distribuídos desordenadamente nas seções "B" e "C"
A sequência dos vagões atrás da locomotiva compondo o trem, é selecionada
 de forma aleatória no início da rodada.
A capacidade de cada uma das seções da disposição deve ser obedecida fielmente,
 conforme o formato escolhido (5-3-3)

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    20.10
        primeira versão.
"""
from random import shuffle, seed
seed(123)
A, B, C, D = "ABCD"


class Shunting:
    def __init__(self):
        convoy = list(range(1, 9))
        shuffle(convoy)
        convoy = [[], convoy[:5], convoy[5:], []]
        self.sections = {name: cars for name, cars in zip("ABCD", convoy)}

    def __repr__(self):
        def s(idx):
            c = self.sections
            return int("".join(str(al)for al in c[idx]) or 0)
        return f" -> A> {s(A):03} <-> B> {s(B):05} <-> C> {s(C):03} <-> D> {s(D):03} <- "

    def move(self, fro, siz, to, cnv):
        s = self.sections
        sec_fro = s[A] if fro == A else s[A]+s[fro]
        if (siz + len(s[to])-cnv) > (5 if to == B else 3):
            print(f"faulty, {fro}, siz, {siz}, to, {to}, len(s[to]), {len(s[to])},"
                  f" cnv, {cnv}, cvy {len((sec_fro[:siz])[cnv:])}"
                  f" tst, {siz + len(s[to])-cnv}, (5 if to == B else 3), {5 if to == B else 3}, s[to], {s[to]} ")
            return
        cvy, s[fro] = sec_fro[:siz], sec_fro[siz:]
        s[to] = (cvy[cnv:] + s[to])[:5 if to == B else 3]
        s[A] = cvy[:cnv]

    def go(self, moves):
        moves = moves.upper()
        moves_ = [moves[i:i+4] for i in range(0, len(moves), 4)]
        [self.move(fro, int(siz), to, int(cnv)) for fro, siz, to, cnv in moves_]


if __name__ == '__main__':
    shu = Shunting()
    print(shu)
    # shu.move(B, 3, D)
    shu.go("B1D0c1b0c2d0d1c0d2c0b3d0c3b0b5c3c4b0b3c1c4b0d1c0b5c4d5b0")
    # shu.go("B1D0c1b0c2d0d1c0d2c0b4d1a1b0d3b0")
    # shu.go("B1D0c1bc2dd1cd2cb1db2dc3bd2cd1cb3d")
    print(shu)

