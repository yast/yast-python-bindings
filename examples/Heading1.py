# encoding: utf-8

from yast import *
class Heading1Client:
    def main(self):
      UI.OpenDialog(VBox(Heading("This Is a Heading."), PushButton("&OK")))
      UI.UserInput()
      UI.CloseDialog()


Heading1Client().main()

