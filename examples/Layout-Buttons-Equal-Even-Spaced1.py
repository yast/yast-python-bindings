# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class LayoutButtonsEqualEvenSpaced1Client:
    def main(self):
      # Layout example:
      #
      # Build a dialog with three equal sized buttons.
      #
      # The equal `HWeight()s will make the buttons equal sized.
      # When resized larger, all buttons will retain their size.
      # Excess space will go to the HStretch() widgets between the
      # buttons, i.e. there will be empty space between the buttons.

      UI.OpenDialog(
        HBox(
          HWeight(1, PushButton(Opt("default"), "&OK")),
          HStretch(),
          HWeight(1, PushButton("&Cancel everything")),
          HStretch(),
          HWeight(1, PushButton("&Help"))
        )
      )

      UI.UserInput()
      UI.CloseDialog()


LayoutButtonsEqualEvenSpaced1Client().main()

