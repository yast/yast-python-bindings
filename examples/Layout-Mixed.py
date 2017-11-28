# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class LayoutMixedClient:
    def main(self):
      # Layout example:
      #
      # Build a dialog with three widgets with different weights and
      # two widgets without any weight.
      #
      # All widgets will get at least their "nice size". The weighted
      # ones may get even more to maintain their share of the overall
      # weight.
      #
      # Upon resize all widgets will resize to maintain their
      # respective weights at all times. The non-weighted widgets will
      # retain their "nice size" regardless whether or not they are
      # stretchable.
      #

      UI.OpenDialog(
        HBox(
          HWeight(33, PushButton(Opt("default"), "OK\n33%")),
          PushButton(Opt("hstretch"), "Apply\nNo Weight"),
          HWeight(33, PushButton("Cancel\n33%")),
          PushButton("Reset to defaults\nNo Weight"),
          HWeight(66, PushButton("Help\n66%"))
        )
      )

      UI.UserInput()
      UI.CloseDialog()


LayoutMixedClient().main()

