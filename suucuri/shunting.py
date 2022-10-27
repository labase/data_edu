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
        convoy = [[], convoy[:SB], convoy[SB:], []]
        self.sections = {name: cars for name, cars in zip("ABCD", convoy)}

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
        s[A], s[to] = a_plus_to[:siz], a_plus_to[siz:]

    def go(self, moves):
        """Recebe uma sequência de comados de mover

        :param moves: texto com duplas indicando a seção e o ponto de desacoplamento.
        :return: None
        """
        moves = moves.upper()
        moves_ = [moves[i:i+2] for i in range(0, len(moves), 2)]
        [self.move(fro, int(siz)) for fro, siz, in moves_]

    def self_go(self, total=10, elenco=7):
        """Recebe uma sequência de comados de mover

        :param total: tamanho total da sequência de tentativas.
        :return: None
        """
        def avante(ordem, base):
            ordem -= 1
            if ordem:
                for algarismo in range(base):
                    for casa in avante(ordem, algarismo):
                        yield f"{casa}{algarismo}"
            else:
                yield ""

        moves = "b0 b1 c0 c1 c2 d0 d2".split()
        acerto = [0]*total
        # moves = "b0 b1 b2 c0 c1 c2 d0 d1 d2".split()
        tentativas = range(len(moves)**total)
        ordens = [7**order for order in range(total)]
        for valor in tentativas:
            vec = [(valor // ordem) % 7 for ordem in ordens]
            print("".join(moves[idx] for idx in vec))


if __name__ == '__main__':
    shu = Shunting()
    print(shu)
    # shu.go("c1d0b2d0d1c0d1b3a3d1c3b1c2b1d2c1b3c1a1d0b3d3a3b0c2b0")
    shu.go("b1c0b1d0b1c1c2b1d2b0")
    shu.self_go(3, 3)
    print(shu)
