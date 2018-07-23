from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class SpecialWidgetClient:
    def main(self):
      # Build a dialog with a "special" widget - one that may not be supported
      # by all UIs.


      # Ask the UI whether or not it supports this widget.

      if UI.HasSpecialWidget("DummySpecialWidget"):
        # Only create a dialog with this kind of widget if it is supported

        UI.OpenDialog(
          VBox(DummySpecialWidget(), PushButton(Opt("default"), "&OK"))
        )
      else:
        # Always provide a fallback: Either try to create a simpler dialog
        # without the special widget, or terminate with an error message.

        UI.OpenDialog(
          VBox(
            Label("Special Widget not supported!"),
            PushButton(Opt("default"), "&Oops!")
          )
        )

      UI.UserInput()
      UI.CloseDialog()


SpecialWidgetClient().main()

