# encoding: utf-8

from yast import *
class VBox1Client:
    def main(self):
      UI.OpenDialog(
        VBox(PushButton("First"), PushButton("Second"), PushButton("Third"))
      )
      UI.UserInput()
      UI.CloseDialog()


VBox1Client().main()

