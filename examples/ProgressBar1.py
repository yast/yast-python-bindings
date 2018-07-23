from __future__ import unicode_literals
# encoding: utf-8

# Simple ProgressBar example
from yast import import_module
import_module('UI')
from yast import *
class ProgressBar1Client:
    def main(self):
      max_progress = 7
      progress = 0

      UI.OpenDialog(
        VBox(
          ProgressBar(Id("pr"), "Sample progress bar", max_progress, progress),
          PushButton(Id("next"), "Next"),
          Right(PushButton(Id("close"), "&Close"))
        )
      )


      while progress < max_progress:
        button = UI.UserInput()

        if button == "next":
          progress = progress + 1
          UI.ChangeWidget(Id("pr"), "Value", progress)
          UI.ChangeWidget(
            Id("pr"),
            "Label",
            ycpbuiltins.sformat("Progress %1 of %2", progress, max_progress)
          )
        elif button == "close":
          break

      UI.CloseDialog()


ProgressBar1Client().main()

