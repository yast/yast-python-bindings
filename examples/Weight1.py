# encoding: utf-8

from yast import *
class Weight1Client:
    def main(self):
      UI.OpenDialog(
        HBox(
          HWeight(1, PushButton("First Button (W: 50)")),
          PushButton("Small Button"),
          HWeight(
            1,
            PushButton(
              "Second Button (Weight 50 - this one determines the total width"
            )
          )
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Weight1Client().main()

