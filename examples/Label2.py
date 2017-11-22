# encoding: utf-8

from yast import *
class Label2Client:
    def main(self):
      UI.OpenDialog(
        VBox(Label("Labels can have\nmultiple lines."), PushButton("&OK"))
      )
      UI.UserInput()
      UI.CloseDialog()


Label2Client().main()

