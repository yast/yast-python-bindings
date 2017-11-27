# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class InfoColorClient:
    def main(self):
      UI.OpenDialog(
        Opt("infocolor"),
        VBox(
          Heading("This is an info dialog."),
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
        Opt("infocolor", "decorated"),
        VBox(Heading("This is a decorated warning dialog."), PushButton("&OK"))
      )
      UI.UserInput()

      UI.CloseDialog()
      UI.CloseDialog()


InfoColorClient().main()

