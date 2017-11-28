# encoding: utf-8

# Animated image example
from yast import import_module
import_module('UI')
from yast import *
class ImageScaledClient:
    def main(self):

      UI.OpenDialog(
        VBox(
          MinSize(
            30,
            10,
            Image(
              Opt("scaleToFit"),
              "/usr/share/wallpapers/Bear.jpg",
              "fallback text"
            )
          ),
          PushButton(Opt("default"), "&OK")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


ImageScaledClient().main()

