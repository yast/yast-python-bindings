from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class ShortcutConflict1Client:
    def main(self):
      # Demo for shortcut checking:
      # Deliberately generate a shortcut conflict.

      UI.OpenDialog(
        HBox(
          PushButton("&OK"),
          PushButton("Also &OK"),
          PushButton("Do Something"),
          PushButton("Quick and Dirty"),
          PushButton("&Cancel")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


ShortcutConflict1Client().main()

