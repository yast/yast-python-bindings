# encoding: utf-8

from yast import *
class MultiLineEdit1Client:
    def main(self):
      UI.OpenDialog(
        VBox(MultiLineEdit("Problem &description:"), PushButton("&OK"))
      )
      UI.UserInput()
      UI.CloseDialog()


MultiLineEdit1Client().main()

