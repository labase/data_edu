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
.. versionadded::    20.10a0
        primeira versão.

.. versionchanged::    20.10a1
        comando em separado por seção.

.. versionadded::    20.11a0
        Continua após um arranjo de seções.
"""
from random import shuffle, seed
seed(123)
A, B, C, D = "ABCD"
# SA, SB, SC, SD = 3, 5, 3, 3
"""Comprimento das seções dos trilhos"""
# CONVOY = 8
"""Número de vagões no total"""
SA, SB, SC, SD = 2, 3, 1, 1
"""Comprimento das seções dos trilhos"""
CONVOY = 3
"""Número de vagões no total"""


class Shunting:
    def __init__(self):
        """Simula a manobra de um trem quatro seções A, B, C, D.

        Inicia colocando aleatoriamente oito vagões, cinco na seção B e três na C.
        """
        convoy = list(range(1, CONVOY+1))
        shuffle(convoy)
        self.convoy = [[], convoy[:SB], convoy[SB:], []]
        self.sections = {name: cars for name, cars in zip("ABCD", self.convoy)}
        self.best = []

    def park(self, park=None):
        """Estaciona os vagões em posição inicial.

        :param park: vagões no início da sequência de tentativas.
        :return: None
        """
        self.sections = park or {name: cars for name, cars in zip("ABCD", self.convoy)}

    def __repr__(self):
        """Formata a apresentação dos vagões.

        :return: um texto formatado mostrando a disposição dos vagões
        """
        def s(idx):
            c = self.sections
            return int("".join(str(al)for al in c[idx]) or 0)
        format_string = " -> A>  {{:0{sa}}} <-> B> {{:0{sb}}} <-> C> {{:0{sc}}} <-> D> {{:0{sd}}} <- "
        format_string = format_string.format(sa=SA, sb=SB, sc=SC, sd=SD)
        # return f" -> A> {s(A):05} <-> B> {s(B):05} <-> C> {s(C):03} <-> D> {s(D):03} <- "
        return format_string.format(s(A), s(B), s(C), s(D))

    def move(self, to, siz):
        """Move o trem da seção A para a seção destino, desacopla e volta.

        :param to: a seção que vai receber o trem.
        :param siz: a distância a partir da locomotiva que o trm vai desacoplar.
        :return: None
        """
        s = self.sections
        a_plus_to = s[A] + s[to]
        size_a_p_to = len(a_plus_to)
        if (size_a_p_to-siz) > (SB if to == B else SC) or (siz > SA):
            # print(f"faulty, siz, {siz}, to, {to}, len(s[to]), {len(s[to])},"
            #       f" (5 if to == B else 3), {SB if to == B else SC}, s[to], {s[to]} ")
            return
        self.sections[A], self.sections[to] = a_plus_to[:siz], a_plus_to[siz:]

    def go(self, moves):
        """Recebe uma sequência de comados de mover

        :param moves: texto com duplas indicando a seção e o ponto de desacoplamento.
        :return: índice da adequação da resposta
        """
        moves = moves.upper()
        moves_ = [moves[i:i+2] for i in range(0, len(moves), 2)]
        [self.move(fro, int(siz)) for fro, siz, in moves_]
        # return sum((SB-pos+1)*SB*(CONVOY-int(carro)) for pos, carro in enumerate(self.sections[B]))
        return sum(10**(SB-pos-1)*(CONVOY-(carro-1)) for pos, carro in enumerate(self.sections[B]))

    def self_go(self, park=None, start=0, total=10):
        """Recebe uma sequência de comados de mover

        :param park: vagões no início da sequência de tentativas.
        :param start: numeral referente à sequência de tentativas.
        :param total: tamanho total da sequência de tentativas.
        :return: None
        """
        moves = "b0 b1 c0 c1 c2 d0 d2".split()
        # moves = "b0 b1 b2 c0 c1 c2 d0 d1 d2".split()
        prk = park or dict(self.sections)
        base = len(moves)
        tentativas = range(start, base**total)
        ordens = [base**order for order in range(total)]
        print(f"tentativas {tentativas} ordens {ordens} park {prk}")
        maxi = 0
        for valor in tentativas:
            # self.park(park)
            self.sections = dict(prk)
            # vec = [(valor // ordem) % 7 for ordem in ordens]
            # roteiro = "".join(moves[idx] for idx in vec)
            roteiro = "".join(moves[(valor // ordem) % 7] for ordem in ordens)
            fit = self.go(roteiro)
            if fit > maxi:
                self.best = []
                maxi = fit
            if fit >= maxi:
                self.best.append((fit, valor, roteiro, dict(self.sections), prk))
        [print(good) for good in self.best]


def _main():
    # (320, 70400, 'b1d0b1c0b1c2b0', {'A': [], 'B': [1, 2], 'C': [], 'D': [3]})
    # (320, 105022, 'b1c0b1d0b1d2b0', {'A': [], 'B': [1, 2], 'C': [3], 'D': []})

    shu = Shunting()
    print(shu)
    shu.go("b1c0b1d0b1c2b1")
    print(shu)


def main(tt=7):
    # (320, 70400, 'b1d0b1c0b1c2b0', {'A': [], 'B': [1, 2], 'C': [], 'D': [3]})
    # (320, 105022, 'b1c0b1d0b1d2b0', {'A': [], 'B': [1, 2], 'C': [3], 'D': []})

    shu = Shunting()
    shu.park({'A': [1], 'B': [3], 'C': [], 'D': [2]})
    print(shu)
    # shu.go("b1d0b1c2b0d1b0")
    shu.self_go(total=tt)
    print(shu)


def main_(tt=7):
    # (320, 70400, 'b1d0b1c0b1c2b0', {'A': [], 'B': [1, 2], 'C': [], 'D': [3]})
    # (320, 105022, 'b1c0b1d0b1d2b0', {'A': [], 'B': [1, 2], 'C': [3], 'D': []})

    shu = Shunting()
    print(shu)
    # shu.move(B, 1)
    # shu.move(C, 0)
    # print(shu.go("b1c0b1d0"))
    # shu.go("c1d0b2d0d1c0d1b3a3d1c3b1c2b1d2c1b3c1a1d0b3d3a3b0c2b0")
    # shu.go("b1c0b1d0b1c1c2b1d2b0")
    shu.self_go(total=tt)
    # shu.self_go({'A': [], 'B': [1, 2], 'C': [], 'D': [3]}, 70400,  9)
    # shu.self_go({'A': [], 'B': [1, 2], 'C': [], 'D': [3]}, 0,  7)
    print(shu)


if __name__ == '__main__':
    # 3515835, 'b1d0b1c0b1d2b1c2b0'
    # 5130315, 'b1c0b1d0b1c2b1d2b0'
    #  105022, 'b1c0b1d0b1d2b0'
    import timeit
    result = timeit.timeit(stmt='main(2)', globals=globals(), number=1)
    print(f"Execution time is {result} seconds")
