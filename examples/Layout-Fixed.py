# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class LayoutFixedClient:
    def main(self):
      # Layout example:
      #
      # Build a dialog with three widgets without any weights.
      #
      # Each widget will get its "nice size", i.e. the size that makes
      # the widget's contents fit into it.
      #
      # Upon resize the widgets will keep their sizes if enlarged
      # (since none of them is stretchable), i.e. there will be empty
      # space to the right.
      #

      UI.OpenDialog(
        HBox(
          PushButton(Opt("default"), "OK"),
          PushButton("Cancel everything"),
          PushButton("Help")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


LayoutFixedClient().main()

