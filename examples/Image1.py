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
            "/usr/share/YaST2/theme/current/wallpapers/welcome.jpg",
            "fallback text"
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      if UI.WidgetExists(Id("image")):
        UI.ChangeWidget(Id("image"), "Enabled", False)
        UI.UserInput()
        UI.ChangeWidget(Id("image"), "Enabled", True)
        UI.UserInput()
      else:
        ycpbuiltins.y2error("No such widget id")
      UI.CloseDialog()


Image1Client().main()

