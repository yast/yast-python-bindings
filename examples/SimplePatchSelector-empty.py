# encoding: utf-8

# Simple example for SimplePatchSelector
from yast import *
class SimplePatchSelectorEmptyClient:
    def main(self):
      if not UI.HasSpecialWidget("SimplePatchSelector"):
        UI.OpenDialog(
          VBox(
            Label(
              "Error: This UI doesn't support the SimplePatchSelector widget!"
            ),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      UI.OpenDialog(
        Opt("defaultsize"),
        Term("SimplePatchSelector", Id("selector"))
      )
      input = UI.RunPkgSelection(Id("selector"))
      UI.CloseDialog()

      ycpbuiltins.y2milestone("Input: %1", input)


SimplePatchSelectorEmptyClient().main()

