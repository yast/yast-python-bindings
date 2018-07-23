from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Frame2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Frame(
            "CPU &Speed",
            RadioButtonGroup(
              VBox(
                Left(RadioButton("Normal")),
                Left(RadioButton("Overclocked")),
                Left(RadioButton("Red Hot")),
                Left(RadioButton("Melting", True))
              )
            )
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Frame2Client().main()

