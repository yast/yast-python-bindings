# encoding: utf-8
from yast import *

class ComboBoxEmptyClient:
    def main(self):
      UI.OpenDialog(
        VBox(ComboBox("Select your Pizza:", [""]), PushButton("&OK"))
      )
      UI.UserInput()
      UI.CloseDialog()

ComboBoxEmptyClient().main()
