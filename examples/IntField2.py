# encoding: utf-8

# Simple IntField example
from yast import import_module
import_module('UI')
from yast import *
class IntField2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          IntField(Id("perc"), "Percentage:", 0, 100, 50),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.ChangeWidget("perc", "Value", 42)
      UI.UserInput()

      percentage = UI.QueryWidget("perc", "Value")
      UI.CloseDialog()

      UI.OpenDialog(
        VBox(
          Label(ycpbuiltins.sformat("You entered: %1%%", percentage)),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


IntField2Client().main()

