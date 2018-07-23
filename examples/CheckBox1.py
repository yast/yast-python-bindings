from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

class CheckBox1Client:
    def main(self):
      UI.OpenDialog(CheckBox("A &checked check box\nwith multi-line", True))
      UI.UserInput()
      UI.CloseDialog()

CheckBox1Client().main()
