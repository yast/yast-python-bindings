# encoding: utf-8

# Simple example for MinWidth widget
from yast import import_module
import_module('UI')
from yast import *
class MinWidth1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          # SelectionBox blown up with MinWidth
          MinWidth(40, SelectionBox("", ["Napoli", "Funghi", "Salami"])),
          # All hstretchable widgets in the same VBox will get
          # at least as wide as specified with MinWidth
          SelectionBox("", ["Napoli", "Funghi", "Salami"]),
          # The same SelectionBox with default width
          # `Left is necessary to take away horizontal stretchability
          Left(SelectionBox("", ["Napoli", "Funghi", "Salami"])),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MinWidth1Client().main()

