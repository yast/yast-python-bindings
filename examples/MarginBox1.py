from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class MarginBox1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MarginBox(10, 2, Label("Hello, World!")),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MarginBox1Client().main()

