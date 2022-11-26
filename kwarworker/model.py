#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL-3 <https://bit.ly/gpl_v3>`__.
# SPDX-License-Identifier: (GPL-3.0-or-later AND LGPL-2.0-only) WITH bison-exception
"""Lida com o gerenciamento de arquivos em vários locais.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11a0
        primeira versão @22
        remove ltk @24
        salva corretamente, gpl atual @25
"""
import json
from base64 import decodebytes as dcd
import base64
from datetime import datetime
from ltk import LTK

from browser import ajax
TIMESTAMP = '@{:%Y-%m-%d %H:%M}'
PR, PK, MD = "data_edu", "kwarworker/_code", "master_ola.py"


class Github:
    VSN = 0

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
        # print("send_request", self.rest.format(owner=self.user, repo=self.repo, path=path))
        req.open(modo, self.rest.format(owner=self.user, repo=self.repo, path=path), True)
        # req.set_header('content-type', "application/vnd.github+json;charset=UTF-8")
        req.set_header('accept', "application/vnd.github+json")
        req.set_header('authorization', f"token {LTK}")
        req.bind('complete', complete)
        req.send(data) if data else req.send()

    def get_file_contents(self, path, callback):
        def complete(request):
            text = json.loads(request.text)
            self.sha = text['sha']
            text = text['content'].replace("\n", '')
            text = str.encode(text)
            text = text + b'===='
            lens = len(text)
            lens = lens - (lens % 4 if lens % 4 else 4)
            self.text = base64.b64decode(text[:lens]).decode("utf-8")
            # print("complete", self.sha, self.text[-40:])
            callback(self)
        self.send_request(path, "GET", complete)

    def update_file_(self, path, comment, decoded_content, callback=None):
        Github.VSN += 1
        path += f"{Github.VSN}"
        data = dict(message=comment, content=decoded_content)
        data = json.dumps(data)
        # print("update_file", path, self.sha, "PUT", callback, data)
        self.send_request(path, "PUT", callback or (lambda *_: None), data)

    def update_file(self, path, comment, decoded_content, callback=None):
        def get(_):
            # sh = '7d43eb2905d728cd66ff41cc097c3fbe29b351fe'
            data = dict(message=comment, content=decoded_content, sha=self.sha)
            # print("update_file", path, self.sha, "PUT", callback, data)
            data = json.dumps(data)
            self.send_request(path, "PUT", callback or (lambda *_: None), data)
        self.get_file_contents(path, get)


class Model:
    def __init__(self, token=None):
        g = Github(token)
        self.user = g.get_user("labase")
        self.repo = None

    def get_file_contents(self, callback, project=PR, packager=PK, moduler=MD):
        self.repo = self.user.get_repo(project)
        path = "{}/{}" if packager else "{}{}"
        # print("get_file_contents ", project, path.format(packager, moduler))
        return self.repo.get_file_contents(path.format(packager, moduler), callback)

    def save_file(self, decoded_content, project=PR, packager=PK, moduler=MD, comment=None, callback=None):
        path = "{}/{}" if packager else "{}{}"
        filename = path.format(packager, moduler)

        def do_save(_):
            timestamp = TIMESTAMP.format(datetime.now())
            _comment = comment if comment else "Saved {} {}".format(filename, timestamp)
            fmt = "{}" if filename.startswith('/') else "{}"
            encodedBytes = base64.b64encode(decoded_content.encode("utf-8"))
            encodedStr = str(encodedBytes, "utf-8")
            # print("do save", fmt, filename, fmt.format(filename))
            self.repo.update_file(fmt.format(filename), _comment, encodedStr, callback=callback)

        self.repo = self.user.get_repo(project)
        # print("save_file ", project, filename)
        self.repo.get_file_contents(filename, do_save)
        return comment
