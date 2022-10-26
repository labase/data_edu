#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa Suucurijuba
# Copyright 2010–2022 Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.activufrj.nce.ufrj.br>`__; `GPL <http://j.mp/GNU_GPL3>`__.
"""
Hitori é um jogo de eliminação de números, jogado em uma grade de quadrados, e ao contrário do Sudoku e do Kakuro,
os enigmas de Hitori começam com todos os números na grade. O objetivo é eliminar pintando algumas células de modo que
não haja nenhum número duplicado em nenhuma fileira ou coluna; além disso, os quadrados eliminados (pintados)
não devem tocar-se vertical ou horizontalmente e podem tocar-se apenas na diagonal;
enquanto que todos os quadrados não pintados devem estar conectados horizontal ou verticalmente para criar
uma única área contígua.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    20.10
        Initial concept.
"""
from random import shuffle, seed
MAX = 6
FMT = "  {:1}"*(MAX-1)
__version__ = "22.10"
seed(123)


class Hitori:
    def __init__(self):
        self.last = last = (MAX-1)
        row = list(range(1, MAX)) * last
        shuffle(row)
        self.rows = [row[last*a_row:last*a_row + last] for a_row in range(MAX-1)]
        # print(self.rows)

    def __repr__(self):
        return "\n".join([FMT.format(*row) for row in self.rows])

    def go(self):
        print("Hikori")
        wrong_r = [[num if row.count(num) == 1 else -num for num in row]
                   for row in self.rows if len(set(row)) != self.last]
        print("wrong rows", wrong_r)
        cols = [list(col) for col in zip(*self.rows)]
        wrong_c = [[num if row.count(num) == 1 else -num for num in row]
                   for row in cols if len(set(row)) != self.last]
        print("wrong columns", wrong_c)


if __name__ == '__main__':
    h = Hitori()
    print(h)
    h.go()
