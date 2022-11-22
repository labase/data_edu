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
from browser import bind, self
import aiol as aio
worker = self
SL = 2


class Guajajara:
    INDIO = None

    def __init__(self, name="y"):
        Guajajara.INDIO = self
        self.name = name
        self.espera = True
        self.andar = True
        self.block = []
        self.bk = None

    def marca(self):
        self.block.append(False)  # (aio.Future())
        return len(self.block)-1

    async def inicio(self):
        pass

    async def manda(self, cmd, block):
        self.bk = aio.Future()
        print("manda")
        worker.send(f"{cmd}")
        # wev = await aio.event(worker, "message")
        # print(wev.target)
        # self.block[block].set_result(False)

    def done(self):
        self.bk.set_result(True)
        print("done")

    async def esperar(self, block):
        return await self.block[block]

    async def anda(self):
        block = self.marca()
        aio.run(self.manda("s", block))
        # await aio.sleep(SL)
        # await aio.event(worker, "message")
        print("anda bk", await self.bk)
        return self.bk

        # return self.block[block]

    def direita(self):
        block = self.marca()
        aio.run(self.manda("o", block))
        # self.esperar(block)


class Ymara(Guajajara):
    async def inicio(self):
        await self.anda()
        await self.anda()
        await self.anda()
        # self.bk = aio.Future()
        # self.bk.set_result(True)
        # await self.bk
        # self.anda()
        # await aio.sleep(SL)
        '''self.anda()
        self.direita()
        self.direita()
        self.direita()'''


@bind(self, "message")
def message(cmd):
    """Handle a message sent by the main script.
    evt.data is the message body.
    """
    # aio.run(runner())
    if cmd.data == "_inicio_":
        Ymara()
        print("inicio")
        aio.run(Guajajara.INDIO.inicio())

    else:
        print("msg done")
        Guajajara.INDIO.done()


async def runner():
    """Handle a message sent by the main script.
    evt.data is the message body.
    """
    if True:
        [self.send("s") for _ in range(8)]
        await aio.sleep(SL)
        [self.send("l") for _ in range(8)]
        await aio.sleep(SL)

        [self.send("n") for _ in range(4)]
        await aio.sleep(SL)

        [self.send("o") for _ in range(4)]
    # except ValueError:
    #     self.send('Please write two numbers')
