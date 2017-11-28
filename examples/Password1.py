# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Password1Client:
    def main(self):
      UI.OpenDialog(VBox(Password("Enter password:"), PushButton("&OK")))
      UI.UserInput()
      UI.CloseDialog()


Password1Client().main()

