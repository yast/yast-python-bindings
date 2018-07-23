from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Label1CsClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label("\u011B\u0161\u010D\u0159\u017E\u00FD\u00E1\u00ED\u02C7"),
          PushButton("&OK\u011B\u0161")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Label1CsClient().main()

