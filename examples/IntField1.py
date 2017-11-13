# encoding: utf-8

from yast import *
class IntField1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          IntField("Percentage:", 0, 100, 50),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


IntField1Client().main()

