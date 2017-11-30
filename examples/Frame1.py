# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Frame1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Frame("Hey! I&mportant!", Label("Hello, World!")),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Frame1Client().main()

