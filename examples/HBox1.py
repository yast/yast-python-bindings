# encoding: utf-8

from yast import *
class HBox1Client:
    def main(self):
      UI.OpenDialog(
        HBox(PushButton("First"), PushButton("Second"), PushButton("Third"))
      )
      UI.UserInput()
      UI.CloseDialog()


HBox1Client().main()

