from __future__ import unicode_literals
# encoding: utf-8

# Advanced Slider + BarGraph example:
#
# Windows partition splitter.
from yast import import_module
import_module('UI')
from yast import *
class WinResizerClient:
    def main(self):
      # Check for availability of required widgets

      if not UI.HasSpecialWidget("Slider") or not UI.HasSpecialWidget("BarGraph"):
        UI.OpenDialog(
          VBox(
            Label(
              "Error: This UI doesn't support the required special widgets!"
            ),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      # Initialize values

      unit = "MB"
      win_used = 350
      total_free = 1500
      min_free = 50
      linux_min = 300
      linux_size = 800
      win_free = total_free - linux_size


      # Create the dialog

      UI.OpenDialog(
        VSquash(
          VBox(
            HSpacing(50), # force width
            Left(Label("Now:")),
            BarGraph(
              Opt("vstretch"),
              [win_used, total_free],
              [
                "Windows\nused\n%1 " + unit,
                "Windows\nfree\n%1 " + unit
              ]
            ),
            VSpacing(2),
            Left(Label("After installation:")),
            BarGraph(
              Id("graph"),
              Opt("vstretch"),
              [win_used, win_free, linux_size],
              [
                "Windows\nused\n%1 " + unit,
                "Windows\nfree\n%1 " + unit,
                "Linux\n%1 "+ unit
              ]
            ),
            Slider(
              Id("linux_size"),
              Opt("notify"),
              "Linux (" + unit + ")",
              linux_min,
              total_free - min_free,
              linux_size
            ),
            PushButton(Id("close"), Opt("default"), "&Close")
          )
        )
      )

      # Event processing loop - left only via the "close" button
      # or the window manager close button / function.

      widget = None
      while True:
        widget = UI.UserInput()

        if widget == "linux_size":
          linux_size = UI.QueryWidget(Id("linux_size"), "Value")

          win_free = total_free - linux_size
          UI.ChangeWidget(
            Id("graph"),
            "Values",
            [win_used, win_free, linux_size]
          )
        if widget == "close" or widget == "cancel":
          break


      UI.CloseDialog()


WinResizerClient().main()

