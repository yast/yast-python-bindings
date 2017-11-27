# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Label1JaClient:
    def main(self):
      UI.OpenDialog(VBox(Label("\u5B8C\u6642"), PushButton("&OK\u5B8C\u6642")))
      UI.UserInput()
      UI.CloseDialog()


Label1JaClient().main()

