# encoding: utf-8

# Simple example for TimeField
from yast import import_module
import_module('UI')
from yast import *
class TimeField1Client:
    def main(self):
      UI.OpenDialog(
        VBox(TimeField(Id("time"), "Time:", "13:15:00"), PushButton("&OK"))
      )
      UI.UserInput()
      UI.CloseDialog()


TimeField1Client().main()

