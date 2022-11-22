# -*- coding: UTF8 -*-
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Dizendo olá para a tribo.
.. versionadded::    22.11a0
        primeira versão.
"""
import suucury
# import suucury
print("ola")


class Ola(suucury.Suucury):
    async def inicia_a_jornada(self):
        print("Ola inicia_a_jornada")

        await self.leste()
        await self.aguarda()
        await self.leste()
        await self.aguarda()
        await self.leste()
        await self.aguarda()


Ola()
