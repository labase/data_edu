#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `LABASE <http://labase.selfip.org/>`__; `GPL <http://is.gd/3Udt>`__.
# SPDX-License-Identifier: (GPLv3-or-later AND LGPL-2.0-only) WITH bison-exception
"""Lida com o gerenciamento de arquivos em vários locais.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11a0
        primeira versão @22
"""
import json
from base64 import decodebytes as dcd
from datetime import datetime

from browser import ajax
LTK = ""  # Labase 09-05-22
TIMESTAMP = '@{:%Y-%m-%d %H:%M}'
PR, PK, MD = "data_edu", "kwarworker/_code", "ola.py"


class Github:
    def __init__(self, token=None):
        self.text = ""
        self.sha = ""
        self.token = token
        self.repo = None
        self.user = None
        self.url = ""
        self.rest = "https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    def get_user(self, user):
        self.user = user
        return self

    def get_repo(self, repo):
        self.repo = repo
        return self

    def send_request(self, path, modo, complete, data=None):
        req = ajax.ajax()
        print("send_request", self.rest.format(owner=self.user, repo=self.repo, path=path))
        req.open(modo, self.rest.format(owner=self.user, repo=self.repo, path=path), True)
        req.set_header('content-type', "application/vnd.github+json;charset=UTF-8")
        req.set_header('authorization', f"labase {LTK}")
        req.bind('complete', complete)
        req.send(data)

    def get_file_contents(self, path, callback):
        def complete(request):
            text = json.loads(request.text)
            self.sha = text['sha']
            text = str.encode(text['content'])
            missing_padding = 4 - len(text) % 4
            text = text + b'=' * missing_padding if missing_padding else text
            self.text = dcd(text).decode("utf-8")
            # dcd(str.encode(op.environ[IKT"])).decode("utf-8")
            callback(self)
        self.send_request(path, "GET", complete)

    def update_file(self, path, comment, decoded_content, callback=None):
        def get(request):
            data = dict(message=comment, content=decoded_content, sha=self.sha)
            self.send_request(path, "POST", callback or (lambda *_: None), data)
            text = str.encode(json.loads(request.text)['content'])
            missing_padding = 4 - len(text) % 4
            text = text + b'=' * missing_padding if missing_padding else text
            self.text = dcd(text).decode("utf-8")
            # dcd(str.encode(op.environ[IKT"])).decode("utf-8")
        self.get_file_contents(path, get)


class Model:
    def __init__(self, token=None):
        g = Github(token)
        self.user = g.get_user("labase")
        self.repo = None

    def get_file_contents(self, callback, project=PR, packager=PK, moduler=MD):
        self.repo = self.user.get_repo(project)
        path = "{}/{}" if packager else "{}{}"
        print("get_file_contents ", project, path.format(packager, moduler))
        return self.repo.get_file_contents(path.format(packager, moduler), callback)

    def save_file(self, decoded_content, project=PR, packager=PK, moduler=MD, comment=None, callback=None):
        path = "{}/{}" if packager else "{}{}"
        filename = path.format(packager, moduler)

        def do_save(_):
            timestamp = TIMESTAMP.format(datetime.now())
            _comment = comment if comment else "Saved {} {}".format(filename, timestamp)
            self.repo.update_file("/{}".format(filename), _comment, decoded_content, callback=callback)

        self.repo = self.user.get_repo(project)
        print("save_file ", project, filename)
        self.repo.get_file_contents(filename, do_save)
        return comment
