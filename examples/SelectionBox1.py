# encoding: utf-8

from yast import *
class SelectionBox1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          SelectionBox("Select your Pizza:", ["Napoli", "Funghi", "Salami"]),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


SelectionBox1Client().main()

