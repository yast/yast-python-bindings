# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class HStretch1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label("Some text goes here"),
          Label("This is some more text, that is quite long, as you can see."),
          HBox(PushButton("&OK"), HStretch())
        )
      )
      ret = UI.UserInput()
      UI.CloseDialog()
      deep_copy(ret)

HStretch1Client().main()

