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
from browser import bind, self as worker
import aio
IMG = "https://i.imgur.com/z7zIJHV.jpg"
ACT = "https://i.imgur.com/ehoPNb1.png"
n, s, o, l, e = list("nsole")


class Suucury:
    def __init__(self, jogo=None):
        self._cmd = None

        @bind(worker, "message")
        def message(cmd):
            """Handle a message sent by the main script.
            evt.data is the message body.
            """
            self._cmd = cmd.data
            aio.run(self.inicia_a_jornada()) if self._cmd == "_inicia_" else None

    async def inicia_a_jornada(self):
        pass

    async def go(self, cmd):
        worker.send(cmd)
        await aio.event(worker, "message")

    async def n(self):
        worker.send(n)
        await aio.event(worker, "message")

    async def s(self):
        worker.send(s)
        await aio.event(worker, "message")

    async def leste(self):
        worker.send(l)
        await aio.event(worker, "message")

    async def oeste(self):
        self.go(o)

    async def aguarda(self, esperado=2):
        await aio.sleep(esperado)

    async def espera(self, esperado):
        while self._cmd != esperado:
            worker.send(e)
            await aio.event(worker, "message")
