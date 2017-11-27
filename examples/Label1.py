# encoding: utf-8

from yast import *
class Label1Client:
    def main(self):
      UI.OpenDialog(VBox(Label("Hello, World!"), PushButton("&OK")))
      UI.UserInput()
      UI.CloseDialog()


Label1Client().main()

