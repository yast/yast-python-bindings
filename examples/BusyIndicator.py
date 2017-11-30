# encoding: utf-8

# Simple BusyIndicator example

from yast import import_module
import_module('UI')
from yast import *

class BusyIndicatorClient:
    def main(self):
      timeout = 3000 # in milisenconds

      UI.OpenDialog(
        VBox(
          BusyIndicator(Id("busy"), "Sample busy indicator", timeout),
          PushButton(Id("alive"), "send &tick"),
          Right(PushButton(Id("close"), "&Close"))
        )
      )


      while True:
        button = UI.TimeoutUserInput(100)

        if button == "alive":
          UI.ChangeWidget(Id("busy"), "Alive", True)
        elif button == "close":
          break

      UI.CloseDialog()

BusyIndicatorClient().main()
