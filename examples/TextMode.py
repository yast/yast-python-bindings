from __future__ import unicode_literals
# encoding: utf-8

# Using UI::TextMode()
from yast import import_module
import_module('UI')
from yast import *
class TextModeClient:
    def main(self):
      msg = "Text mode" if UI.TextMode() else  "GUI mode"
      UI.OpenDialog(VBox(Label(msg), PushButton(Opt("default"), "&OK")))
      UI.UserInput()
      UI.CloseDialog()


TextModeClient().main()

