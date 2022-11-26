#! /usr/bin/env python
# -*- coding: UTF8 -*-
# Este arquivo é parte do programa SuuCuriJuba
# Copyright © 2022  Carlo Oliveira <carlo@nce.ufrj.br>,
# `Labase <http://labase.selfip.org/>`__; `GPL-3 <https://bit.ly/gpl_v3>`__.
# SPDX-License-Identifier: (GPL-3.0-or-later AND LGPL-2.0-only) WITH bison-exception
"""Teste com worker para código controlando jogo.

.. codeauthor:: Carlo Oliveira <carlo@nce.ufrj.br>

Changelog
---------
.. versionadded::    22.11a0
        primeira versão @22
        adiciona botão passo a passo @22
        adiciona botão executa @24
        melhora mensagem salvar, gpl atual @25

.. versionadded::    22.11b0
        executa da trilha principal @26

"""
import json
import sys
from browser import window, ajax, document, timer, run_script as python_runner
from kwarapp import main as k_main
MOD = "master_ola.py"
FROM_WORK = False
widget_code_lr = """
  <div class="script-title" id="title-%s"></div>
  <div class="script-container" id="script-container-%s">
    <div id="script-%s" class="script-editor"></div>
    <div id="result-%s" class="script-result"><pre id="result_pre-%s"></pre></div>
  </div>  
  <button class="script-button" id="run-%s" type="button">Executar</button>
  <button class="script-button" id="clear-%s" type="button">Limpar Console</button>
  <button class="script-button" id="reset-%s" type="button">Reiniciar</button>
  <button class="script-button" id="step-%s" type="button">Passo</button>
"""

widget_code_tb = """
  <div class="script-title" id="title-%s"></div>
  <div class="script-container" id="script-container-%s">
    <div id="script-%s" class="script-editor-long"></div>
    <div id="result-%s" class="script-result-long"><pre id="result_pre-%s"></pre></div>
  </div>  
  <button class="script-button" id="run-%s" type="button">Executar</button>
  <button class="script-button" id="clear-%s" type="button">Limpar Console</button>
  <button class="script-button" id="reset-%s" type="button">Reiniciar</button>
  <button class="script-button" id="step-%s" type="button">Passo</button>
"""


class ScriptStderr:
    def __init__(self, console_pre_id):
        self.__console_pre_id = console_pre_id

    def write(self, err):
        document[self.__console_pre_id].style.color = "red"
        document[self.__console_pre_id].innerHTML = err


class ScriptWidget:

    def __init__(self, script_name=None, main_div_id='', **params):
        """ Creates a widget in a given DIV
        @param params :
          - height: integer in pixels
          - editor_width: in the case of side-by-side arrangement of windows *editor_width* property defines
            the percentage of the code editor panel; the remaining width will be used by the console
          - alignment: either 'left-right' (the default) or 'top-bottom'
          - read_only: False (default) or True; if True, user won't be able to edit the script
          - hide_buttons: False (default) or True; if True, user won't be able to run the script
          - console_height: integer in pixels - height of the console panel
          - name: name of the module to run; by default this widget just runs the whole script; use
            the ``name`` keyword to run ``__main__`` section of a Python script
        """
        m = main_div_id
        self.script_name = script_name
        self.script_div_id = "script-%s" % main_div_id
        self.name_to_run = params.get("name", None)
        self.console_pre_id = "result_pre-%s" % main_div_id
        self.script_path = "_code/"
        self.main_div_id = main_div_id
        self.get_script(None) if script_name else None

        if "alignment" in params and params["alignment"] == 'top-bottom':
            document[main_div_id].innerHTML = widget_code_tb % (m, m, m, m, m, m, m, m, m)
        else:
            document[main_div_id].innerHTML = widget_code_lr % (m, m, m, m, m, m, m, m, m)
            if "editor_width" in params:
                document[self.script_div_id].style.width = params["editor_width"]

        document["run-%s" % main_div_id].bind("click", self.run_script)
        document["clear-%s" % main_div_id].bind("click", self.clear_console)
        document["reset-%s" % main_div_id].bind("click", self.get_script) if script_name else None

        # Set title (number and name) of the script
        index = params.get("index", None)
        title = params.get("title", None)
        if index:
            title_text = "<b>Exemplo %s</b>" % index
            if title:
                title_text += ": %s" % title
            document["title-%s" % main_div_id].innerHTML = title_text

        # Set height of the editor's window
        self.editor = window.ace.edit(self.script_div_id)
        if "height" in params:
            h = "%dpx" % (params["height"])
        else:
            h = "200px"
        self.editor.container.style.height = h
        self.editor.setReadOnly(params.get("read_only", False))

        document[self.script_div_id].style.height = h
        if "console_height" in params:
            document[self.console_pre_id].style.height = "%dpx" % (params["console_height"])
        else:
            document[self.console_pre_id].style.height = h

        # --- Hide buttons (or not)
        if params.get("hide_buttons", False):
            del document["run-%s" % main_div_id]
            del document["clear-%s" % main_div_id]
            del document["reset-%s" % main_div_id]

    def write(self, strn):
        def set_svg():
            _ = document[self.console_pre_id] <= strn

        timer.set_timeout(set_svg, 10)

    def clear_console(self, _):
        document[self.console_pre_id].innerHTML = ""

    def run_script(self, *_):
        def do_run(ct=''):
            msg = json.loads(ct.text)
            print(msg['commit']['message'] if "commit" in msg else 'Falha no salvamento')
            from kwarapp import Kwarwp
            Kwarwp().go()

        def run_now(*_):
            if self.name_to_run is None:
                python_runner(editor.getValue())
            else:
                python_runner(editor.getValue(), self.name_to_run)
        editor = window.ace.edit(self.script_div_id)
        document[self.console_pre_id].style.color = "black"
        sys.stdout = self
        sys.stderr = ScriptStderr(self.console_pre_id)
        if FROM_WORK:
            callback = do_run
            from model import Model
            Model().save_file(decoded_content=editor.getValue(), callback=callback, moduler=MOD)
        else:
            run_now()

    def get_script_callback(self, request):
        editor = window.ace.edit(self.script_div_id)
        # print(request.text)
        editor.setValue(request.text, -1)
        editor.setTheme("ace/theme/dracula")
        # editor.setTheme("ace/theme/solarized_light")
        editor.getSession().setMode("ace/mode/python")

    def get_script(self, _):
        from model import Model
        Model().get_file_contents(self.get_script_callback, moduler=MOD)

    def get_script_(self, _):
        req = ajax.ajax()
        req.open('GET', self.script_path + self.script_name, True)
        req.set_header('content-type', "application/x-www-form-urlencoded;charset=UTF-8")
        req.bind('complete', self.get_script_callback)
        req.send()


def main(pyed="pyedit"):
    _ = ScriptWidget("master_ola.py", pyed, heigh=800, console_height=200, alignment="left-right", title="Olá, tribo!")
    # , editor_width=60)
    k_main()
