# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class InputField1Client:
    def main(self):
      UI.OpenDialog(VBox(InputField("Name:"), PushButton("&OK")))
      UI.UserInput()
      UI.CloseDialog()


InputField1Client().main()

