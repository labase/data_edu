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
from browser import bind, self, aio
SL = 2


@bind(self, "message")
def message(evt):
    """Handle a message sent by the main script.
    evt.data is the message body.
    """
    aio.run(runner())


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
