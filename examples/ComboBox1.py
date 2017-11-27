# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

class ComboBox1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          ComboBox("Select your Pizza:", ["Napoli", "Funghi", "Salami"]),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()

ComboBox1Client().main()
