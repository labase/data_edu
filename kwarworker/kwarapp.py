#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `LABASE <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Teste com worker para script controlando jogo.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11a0
        primeira versão.
"""
from browser import bind, document, worker, html

# Create a web worker, identified by a script id in this page.
myWorker = worker.Worker("worker")
IMG = "https://i.imgur.com/z7zIJHV.jpg"
ACT = "https://i.imgur.com/ehoPNb1.png"


class Kwarwp:
    def __init__(self):
        self.root = document["pydiv"]
        self.root.html = ''
        self.scenario, self.actor, self.x, self.y = None, None, 0, 0
        self.cena()
        self.ator()
        self.cmd = dict(n=self.n, l=self.leste, s=self.s, o=self.oeste, e=self.espera)
        myWorker.send("_inicia_")

        @bind(myWorker, "message")
        def parse(e):
            """Handles the messages sent by the worker."""
            cmd = e.data
            print(cmd)
            self.cmd[cmd]()

        @bind(self.scenario, "click")
        def change(_):
            """Called when the value in one of the input fields changes."""
            # Send a message (here a list of values) to the worker
            # myWorker.send([x.value for x in inputs])
            # self.vai()
            myWorker.send("4")
            print(self.x)

    def cena(self, img=IMG):
        self.scenario = html.DIV(html.IMG(src=img, width="1300px"), style=dict(position="absolute"))
        _ = self.root <= self.scenario

    def ator(self, img=ACT):
        class Ator:
            def __init__(self, elt):
                self.elt = elt
                # self.x, self.y = 0, 0

            @property
            def x(self):
                return self.elt.style.left

            @x.setter
            def x(self, x):
                self.elt.style.left = x

            @property
            def y(self):
                return self.elt.style.top

            @y.setter
            def y(self, y):
                self.elt.style.top = y

        _actor = html.IMG(src=img, width="130px", style=dict(position="absolute", left=0, top=0))
        self.actor = html.DIV(_actor, style=dict(position="absolute", left=0, top=0))
        _ = self.scenario <= self.actor
        return Ator(self.actor)

    def n(self):
        self.y = self.y - 10 if self.y >= 10 else 0
        self.actor.style.top = f"{self.y}px"
        myWorker.send("n")

    def s(self):
        self.y = self.y + 10 if self.y <= 650 else 0
        self.actor.style.top = f"{self.y}px"
        myWorker.send("n")

    def oeste(self):
        self.x = self.x - 10 if self.x >= 10 else 0
        self.actor.style.left = f"{self.x}px"
        myWorker.send("n")

    def leste(self):
        self.x = self.x + 10 if self.x <= 1300 else 0
        self.actor.style.left = f"{self.x}px"
        myWorker.send("n")

    def espera(self, *_):
        self.x += 10
        self.actor.style.left = f"{self.x}px"


def main():
    return Kwarwp()
