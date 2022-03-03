# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class ShortcutConflict6Client:
    def main(self):
      # Demo for shortcut checking:
      # Only exotic characters, not enough valid shortcut characters.

      UI.OpenDialog(
        HBox(
          PushButton(u"&\u00A7\u00A7"),
          PushButton("&???"),
          PushButton("?&??"),
          PushButton("&!!!"),
          PushButton("&***"),
          PushButton("&OK")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


ShortcutConflict6Client().main()

