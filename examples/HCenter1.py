from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class HCenter1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label("This is a long label which makes space"),
          HBox(Label("A"), HCenter(Label("B")), Label("C"))
        )
      )
      UI.UserInput()
      UI.CloseDialog()


HCenter1Client().main()

