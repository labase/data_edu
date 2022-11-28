#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL-3 <https://bit.ly/gpl_v3>`__.
# SPDX-License-Identifier: (GPL-3.0-or-later AND LGPL-2.0-only) WITH bison-exception
"""Teste com worker para script controlando jogo.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11a0
        primeira versão @16
        coloca parsing dentro do Kwarwp init @17
        adiciona passo a passo @22

.. versionadded::    22.11b0
        move trabalhador para constante @26

.. versionadded::    22.11b1
        adiciona trilha de NPC @26
"""
from browser import bind, document, worker, html, aio

IMG = "https://i.imgur.com/z7zIJHV.jpg"
ACT = "https://i.imgur.com/ehoPNb1.png"
YMR = "https://i.imgur.com/iJqmT9V.png"
SLEEP = 0.1
WK = worker.Worker("worker")
NP = worker.Worker("npc")


class Kwarwp:
    def __init__(self, actor="worker"):
        self.root = document["pydiv"]
        self.main_actor = actor
        self.root.html = ''
        self.scenario, self.actor, self.x, self.y = None, {}, 0, 0
        self.cena()
        self.ator(actor)
        # self.wk, self.np = WK, NP

        @bind(self.wk, "message")
        def parsing(e):
            """Handles the messages sent by the worker."""
            oid, cmd = e.data.split()
            # print("got cmd ", cmd)
            aio.run(self.actor[oid].command(cmd))

    def nop(self, *_):
        pass

    def go(self):
        # print("go cmd ", self.wk)
        self.wk.send("_inicia_")

    def done(self, cmd="done"):
        async def _next():
            await aio.event(document["step-pyedit"], "click")
            self.wk.send(cmd)

        aio.run(_next())

    def cena(self, img=IMG):
        self.scenario = html.DIV(html.IMG(src=img, width="1300px"), style=dict(position="absolute"))
        _ = self.root <= self.scenario

    def ator(self, actor, img=ACT, x=0, y=0):
        self.actor[actor] = the_actor = Ator(actor, img=img, x=x, y=y)
        _ = self.scenario <= the_actor
        return Ator(the_actor)


class Ator:
    def __init__(self, oid, img=IMG, x=0, y=0):
        self.oid = oid
        self.wk = worker.Worker(oid)
        _actor = html.IMG(src=img, width="130px", style=dict(position="absolute", left=0, top=0))
        self.x, self.y = x, y
        self.actor = html.DIV(_actor, ID=oid, style=dict(position="absolute", left=0, top=0))
        self._x, self._y = x, y
        self.cmd = dict(n=self.norte, l=self.leste, s=self.sul, o=self.oeste)

        @bind(self.wk, "message")
        def parsing(e):
            """Handles the messages sent by the worker."""
            _oid, cmd = e.data.split()
            # print("got cmd ", cmd)
            aio.run(self.actor[_oid].command(cmd))

    @property
    def x(self):
        return self.actor.style.left

    @x.setter
    def x(self, _x):
        self.actor.style.left = self._x = _x

    @property
    def y(self):
        return self.actor.style.top

    @y.setter
    def y(self, _y):
        self.actor.style.top = self._y = _y

    async def command(self, cmd):
        self.cmd[cmd]() if cmd in self.cmd else None

    def done(self, cmd="done"):
        async def _next():
            await aio.event(document["step-pyedit"], "click")
            self.wk.send(f"{self.oid} done")

        aio.run(_next())

    def norte(self):
        self.y = self.y - 10 if self.y >= 10 else 0
        self.actor.style.top = f"{self.y}px"
        self.done()

    def sul(self):
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
    kwarwp = Kwarwp()
    kwarwp.go()
    return kwarwp
