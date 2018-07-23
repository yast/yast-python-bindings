from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class HBox1Client:
    def main(self):
      UI.OpenDialog(
        HBox(PushButton("First"), PushButton("Second"), PushButton("Third"))
      )
      UI.UserInput()
      UI.CloseDialog()


HBox1Client().main()

