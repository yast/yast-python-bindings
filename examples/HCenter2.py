from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class HCenter2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label("This is a very long label that makes space"),
          HBox(PushButton("Normal"), HCenter(PushButton("HCenter")))
        )
      )
      UI.UserInput()
      UI.CloseDialog()


HCenter2Client().main()

