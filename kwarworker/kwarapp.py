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
        coloca parsing dentro do Kwarwp init
"""
from browser import bind, document, worker, html, aio

# Create a web worker, identified by a script id in this page.
# myWorker = worker.Worker("worker")
IMG = "https://i.imgur.com/z7zIJHV.jpg"
ACT = "https://i.imgur.com/ehoPNb1.png"


class Kwarwp:
    def __init__(self, working="worker"):
        self.root = document["pydiv"]
        self.root.html = ''
        self.scenario, self.actor, self.x, self.y = None, None, 0, 0
        self.cena()
        self.ator()
        self.wk = worker.Worker(working)
        self.cmd = dict(n=self.n, l=self.l, s=self.s, o=self.o)

        @bind(self.wk, "message")
        def parsing(e):
            """Handles the messages sent by the worker."""
            cmd = e.data
            print("got cmd ", cmd)
            # self.cmd[cmd]()
            aio.run(self.command(cmd))

    async def command(self, cmd):
        await aio.sleep(2)
        self.cmd[cmd]()

    def go(self):
        self.wk.send("_inicio_")

    def done(self):
        self.wk.send("done")

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
        self.done()

    def s(self):
        self.y = self.y + 10 if self.y <= 650 else 0
        self.actor.style.top = f"{self.y}px"
        self.done()

    def oeste(self):
        self.x = self.x - 10 if self.x >= 10 else 0
        self.actor.style.left = f"{self.x}px"
        self.done()

    def leste(self):
        self.x = self.x + 10 if self.x <= 1300 else 0
        self.actor.style.left = f"{self.x}px"
        self.done()

    def espera(self, *_):
        self.x += 10
        self.actor.style.left = f"{self.x}px"


def main():
    return Kwarwp()
