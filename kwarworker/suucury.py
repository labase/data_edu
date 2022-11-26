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
        primeira versão @17
        incorpora o método go nos comandos @22

.. versionadded::    22.11b0
        reformula para controle da trilha principal @26
"""
from browser import bind, worker, document
import aio
from kwarapp import Kwarwp
n, s, o, l, e = list("nsole")


class Suucury(Kwarwp):
    def __init__(self, working="worker"):
        super().__init__(working)
        self._cmd = None
        self.worker = self.wk  # worker.Worker(working)
        # print("Suucury __init__", self.wk)

        @bind(self.worker, "message")
        def message(cmd):
            """Handle a message sent by the worker thread.
            evt.data is the message body.
            """
            self._cmd = cmd.data
            # print("Suucury __init__ message", self._cmd)
            aio.run(self.inicia_a_jornada()) if self._cmd == "_inicia_" else None

    async def inicia_a_jornada(self):
        pass

    def done_(self, cmd="done"):
        async def _next():
            await aio.event(document["step-pyedit"], "click")
            self.wk.send(cmd)
        aio.run(_next())

    async def did(self, *_):
        await aio.event(self.worker, "message")

    async def n(self):
        super().n()
        await self.did(n)

    async def s(self):
        super().s()
        await self.did(s)

    async def leste(self):
        super().leste()
        await self.did(l)

    async def oeste(self):
        super().oeste()
        await self.did(o)

    async def aguarda(self, esperado=0.1):
        await aio.sleep(esperado)

    async def espera(self, esperado):
        while self._cmd != esperado:
            worker.send(e)
            await aio.event(worker, "message")
