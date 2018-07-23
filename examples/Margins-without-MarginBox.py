from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class MarginsWithoutMarginBoxClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          HBox(
            HSpacing(10),
            VBox(VSpacing(2), Label("Hello, World!"), VSpacing(2)),
            HSpacing(10)
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MarginsWithoutMarginBoxClient().main()

