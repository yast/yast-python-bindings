# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class SelectionBox5Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          SelectionBox(
            Opt("shrinkable"),
            "Minimalistic selbox (rather ugly): ",
            [
              "Napoli",
              "Funghi",
              "Salami",
              "Quattro Stagioni",
              "Caprese",
              "Mista"
            ]
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


SelectionBox5Client().main()

