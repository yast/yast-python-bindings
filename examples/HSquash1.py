# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class HSquash1Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          VCenter(
            HSquash(
              VBox(
                Left(CheckBox("short")),
                Left(CheckBox("longer")),
                Left(CheckBox("even longer")),
                Left(CheckBox("yet even longer")),
              )
            ) # Makes the VBox nonstretchable horizontally
          ), # Makes the HSquash stretchable vertically
          Left(PushButton("bottom left"))
        )
      )
      UI.UserInput()
      UI.CloseDialog()

HSquash1Client().main()

