# -*- coding: UTF8 -*-
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Dizendo olá para a tribo.
.. versionadded::    22.11a0
        primeira versão @24
"""
import suucury
print("master ola")


class Ola(suucury.Suucury):
    async def inicia_a_jornada(self):
        print("Master Ola inicia_a_jornada")

        await self.leste()
        await self.leste()
        await self.leste()


Ola()