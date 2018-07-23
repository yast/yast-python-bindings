from __future__ import unicode_literals
# encoding: utf-8

# Animated image example
from yast import import_module
import_module('UI')
from yast import *
class ImageAnimatedClient:
    def main(self):

      UI.OpenDialog(
        VBox(
          MinSize(
            30,
            10,
            Image(
              Opt("animated"),
              "/usr/lib/qt3/doc/examples/widgets/trolltech.gif",
              "fallback text"
            )
          ),
          PushButton(Opt("default"), "&OK")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


ImageAnimatedClient().main()

