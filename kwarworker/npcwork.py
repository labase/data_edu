#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL-3 <https://bit.ly/gpl_v3>`__.
# SPDX-License-Identifier: (GPL-3.0-or-later AND LGPL-2.0-only) WITH bison-exception
"""Worker para gerenciar NPC.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11b1
        primeira versão @26
        trilha em ronda @28
"""
import suucury

print("Ativando NPC")


class Npc(suucury.Suucury):
    async def inicia_a_jornada(self):
        print("Ola inicia_a_jornada")
        [await self.leste() for _ in range(8)]
        [await self.sul() for _ in range(8)]
        [await self.oeste() for _ in range(8)]
        [await self.norte() for _ in range(8)]

        # await self.leste()
        # await self.aguarda()
        # await self.leste()
        # await self.aguarda()
        # await self.leste()
        # await self.aguarda()


Npc()
