#!/usr/bin/env python
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

class BarGraph2Client:
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
          HSpacing(80), # force width
          HBox(
            Opt("debugLayout"),
            BarGraph(
              Opt("vstretch"),
              [600, 350, 800],
              ["Windows\nused\n%1 MB", "Windows\nfree\n%1 MB", "Linux\n%1 MB"]
            )
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()

BarGraph2Client().main()
