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
KW = None


class Kwarwp:
    def __init__(self):
        self.root = document["pydiv"]
        self.root.html = ''
        self.scenario, self.actor, self.x, self.y = None, None, 0, 0
        self.cena()
        self.ator()
        self.cmd = dict(n=self.n, l=self.l, s=self.s, o=self.o)
        myWorker.send("4")

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
        _actor = html.IMG(src=img, width="130px", style=dict(position="absolute", left=0, top=0))
        self.actor = html.DIV(_actor, style=dict(position="absolute", left=0, top=0))
        _ = self.scenario <= self.actor

    def n(self):
        self.y = self.y - 10 if self.y >= 10 else 0
        self.actor.style.top = f"{self.y}px"

    def s(self):
        self.y = self.y + 10 if self.y <= 650 else 0
        self.actor.style.top = f"{self.y}px"

    def l(self):
        self.x = self.x - 10 if self.x >= 10 else 0
        self.actor.style.left = f"{self.x}px"

    def o(self):
        self.x = self.x + 10 if self.x <= 1300 else 0
        self.actor.style.top = f"{self.y}px"

    def vai(self, *_):
        self.x += 10
        self.actor.style.left = f"{self.x}px"


@bind(myWorker, "message")
def parse(e):
    """Handles the messages sent by the worker."""
    cmd = e.data
    print(cmd)
    KW.cmd[cmd]()


def main():
    global KW
    KW = Kwarwp()
