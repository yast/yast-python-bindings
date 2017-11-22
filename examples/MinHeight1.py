# encoding: utf-8

# Simple example for MinHeight widget
from yast import *
class MinHeight1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          HBox(
            # SelectionBox blown up with MinHeight
            MinHeight(12, SelectionBox("", ["Napoli", "Funghi", "Salami"])),
            # All vstretchable widgets in the same HBox will get
            # at least as wide as specified with MinHeight
            MinWidth(25, SelectionBox("", ["Napoli", "Funghi", "Salami"])),
            # The same SelectionBox with default width
            # `Top is necessary to take away vertical stretchability
            Top(SelectionBox("", ["Napoli", "Funghi", "Salami"]))
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MinHeight1Client().main()

