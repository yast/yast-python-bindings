# encoding: utf-8

from yast import *
class MarginBox1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MarginBox(10, 2, Label("Hello, World!")),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MarginBox1Client().main()

