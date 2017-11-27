# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class DecoratedClient:
    def main(self):
      UI.OpenDialog(
        Opt("decorated"),
        VBox(
          Label(
            "This Dialog is decorated.\n\n" + "You might not see a difference\n" +
              "if you are using a window manager, though."
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()

      UI.OpenDialog(
        Opt("warncolor"),
        VBox(
          Heading("This is a warning dialog."),
          RichText(
            "This should even work with multi line rich texts. " +
              "Even with <b>bold face</b> or <i>italic</i> or " +
              "<b><i>bold italic</i></b>."
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()

      UI.OpenDialog(
        Opt("warncolor","decorated"),
        VBox(Heading("This is a decorated warning dialog."), PushButton("&OK"))
      )
      UI.UserInput()
      UI.CloseDialog()
      UI.CloseDialog()
      UI.CloseDialog()


DecoratedClient().main()

