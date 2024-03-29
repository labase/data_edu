#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Versão mangada da classe browser.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11a0
        primeira versão.
"""
from unittest.mock import MagicMock


class MMock(MagicMock):
    def __le__(self, _):
        return MagicMock()


class dom(dict):
    head = MMock()

    def __le__(self, _):
        return MagicMock()


class window:
    ace = MMock()


class html:
    DIV = MMock()
    IMG = MMock()

    def __init__(self, *_, **__):
        self.value = ""
        pass

    def __le__(self, _):
        return MagicMock()

    def __call__(self, _):
        return MagicMock()


timer = ajax = worker = self = aio = _aio = bind = run_script = html.IMG = MMock()
document = dom(pydiv=dom())
document.head = dom()
html.DIV = html.STYLE = html.bind = html.H1 = html.H2 = html.A = html.CODE = html.PRE = html
html.style = MMock()
