#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL-3 <https://bit.ly/gpl_v3>`__.
# SPDX-License-Identifier: (GPL-3.0-or-later AND LGPL-2.0-only) WITH bison-exception
"""Worker orquestra a trilha principal.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11b0
        primeira versão @26
"""
from browser import bind, self as worker
import aio
print("Maestro")


class Maestro:
    def __init__(self):
        self._cmd = None
        self.worker = worker

        @bind(worker, "message")
        def message(cmd):
            """Handle a message sent by the main script.
            evt.data is the message body.
            """
            self._cmd = cmd.data
            # print("Maestro message", self._cmd)
            aio.run(self.go(self._cmd))
            # aio.run(self.inicia_a_jornada()) if self._cmd == "_inicia_" else None

    async def go(self, cmd):
        self.worker.send(cmd)
        # await aio.event(self.worker, "message")


Maestro()
