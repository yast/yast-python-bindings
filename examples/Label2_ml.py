# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Label2MlClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label(
            "\u00DF\u00F6\u00F6\u00F6\u00F6\u00F6\u00F6\u00DC\u00DC\u00DC\u00DC\u00DC\u00F6\u00DF\u00DF\u00DF\u00DF\u00E4\u00C4\u00C4\u00C4\u00C4\n" +
              "\u011B\u0161\u010D\u0159\u017E\u00FD\u00E1\u00ED\u02C7\n" +
              "multiple lines."
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Label2MlClient().main()

