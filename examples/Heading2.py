from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Heading2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("This Is a Heading."),
          Label("This is a Label."),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Heading2Client().main()

