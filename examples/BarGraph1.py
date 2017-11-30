#!/usr/bin/env python
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

# BarGraph1.ycp
class BarGraph1Client:
    def main(self):
      if not UI.HasSpecialWidget("BarGraph"):
        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the BarGraph widget!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return

      UI.OpenDialog(
        VBox(
          HSpacing(60), # wider default size
          BarGraph([450, 100, 700]),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()

BarGraph1Client().main()
