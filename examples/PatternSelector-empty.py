# encoding: utf-8

# Simple example for PatternSelector
from yast import *
class PatternSelectorEmptyClient:
    def main(self):
      if not UI.HasSpecialWidget("PatternSelector"):
        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the PatternSelector widget!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      UI.OpenDialog(Opt("defaultsize"), PatternSelector(Id("selector")))
      input = UI.RunPkgSelection(Id("selector"))
      UI.CloseDialog()

      ycpbuiltins.y2milestone("Input: %1", input)


PatternSelectorEmptyClient().main()

