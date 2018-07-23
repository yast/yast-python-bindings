#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from yast import import_module
import_module('UI')
from yast import *
import ycpbuiltins

# Test for UI::Beep()
class BeepClient:
    def main(self):
      UI.OpenDialog(Label("Doing some operations..."))
      ycpbuiltins.sleep(4000)
      UI.CloseDialog()

      UI.Beep()
      UI.OpenDialog(
        VBox(
          Label("Done. Now prooceed to answer the next questions."),
          PushButton("Ok")
        )
      )
      UI.UserInput()
      UI.CloseDialog()

BeepClient().main()
