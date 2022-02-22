# encoding: utf-8

# Simple image example
from yast import import_module
import_module('UI')
from yast import *
class Image1Client:
    def main(self):

      UI.OpenDialog(
        VBox(
          Image(
            Id("image"),
            "/usr/share/grub2/themes/openSUSE/logo.png",
            "fallback text"
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


Image1Client().main()

