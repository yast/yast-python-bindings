# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class LayoutStretchableClient:
    def main(self):
      # Layout example:
      #
      # Build a dialog with three widgets without any weights.
      #
      # Each widget will get its "nice size", i.e. the size that makes
      # the widget's contents fit into it.
      #
      # Upon resize the first and the last widgets will stretch, the
      # center widget will retain its size.
      #
      # The stretchable widgets will get an equal share of the extra
      # space in addition to their "nice size". They are not
      # (generally) of equal size!
      #

      UI.OpenDialog(
        HBox(
          PushButton(Opt("hstretch", "default"), "I am stretchable"),
          PushButton("I am not"),
          PushButton(Opt("hstretch"), "I am stretchable, too")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


LayoutStretchableClient().main()

