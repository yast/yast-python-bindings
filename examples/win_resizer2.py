from __future__ import unicode_literals
# encoding: utf-8

# Advanced Slider + BarGraph example:
#
# Windows partition splitter,
# this time with two sliders
from yast import import_module
import_module('UI')
from yast import *
class WinResizer2Client:
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
      suggested_linux_size = 800
      linux_size = suggested_linux_size
      win_free = (total_free - linux_size)


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
                "Linux\n%1 " + unit
              ]
            ),
            VSpacing(0.5),
            Slider(
              Id("win_free"),
              Opt("notify"),
              "Windows free (" + unit + ")",
              min_free,
              total_free - linux_min,
              win_free
            ),
            VSpacing(0.5),
            Slider(
              Id("linux_size"),
              Opt("notify"),
              "Linux (" + unit + ")",
              linux_min,
              total_free - min_free,
              linux_size
            ),
            VSpacing(0.5),
            HBox(
              HCenter(PushButton(Id("suggest"), "&Default")),
              PushButton(Id("close"), Opt("default"), "&Close")
            )
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
          UI.ChangeWidget(Id("win_free"), "Value", win_free)
        elif widget == "win_free":
          win_free = UI.QueryWidget(Id("win_free"), "Value")
          linux_size = total_free - win_free
          UI.ChangeWidget(
            Id("graph"),
            "Values",
            [win_used, win_free, linux_size]
          )
          UI.ChangeWidget(Id("linux_size"), "Value", linux_size)
        elif widget == "suggest":
          linux_size = suggested_linux_size
          win_free = total_free - linux_size
          UI.ChangeWidget(
            Id("graph"),
            "Values",
            [win_used, win_free, linux_size]
          )
          UI.ChangeWidget(Id("linux_size"), "Value", linux_size)
          UI.ChangeWidget(Id("win_free"), "Value", win_free)
        if widget == "close" or widget == "cancel":
          break

      UI.CloseDialog()


WinResizer2Client().main()

