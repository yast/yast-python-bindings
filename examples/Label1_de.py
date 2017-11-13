# encoding: utf-8

from yast import *
class Label1DeClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label(
            "\u00DF\u00F6\u00F6\u00F6\u00F6\u00F6\u00F6\u00DC\u00DC\u00DC\u00DC\u00DC\u00F6\u00DF\u00DF\u00DF\u00DF\u00E4\u00C4\u00C4\u00C4\u00C4"
          ),
          PushButton("\u00C4&\u00D6\u00E4")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Label1DeClient().main()

