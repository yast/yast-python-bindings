# encoding: utf-8

# Minimalistic example for tab widget
from yast import import_module
import_module('UI')
from yast import *
class DumbTab1Client:
    def main(self):
      if not UI.HasSpecialWidget("DumbTab"):
        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the DumbTab widget!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      UI.OpenDialog(
        VBox(
          DumbTab(
            ["Page 1", "Page 2", "Page 3"],
            RichText(Id("contents"), "Contents")
          ),
          Right(PushButton(Id("close"), "&Close"))
        )
      )

      UI.DumpWidgetTree()

      input = None
      while True:
        input = UI.UserInput()

        if len(input):
          UI.ChangeWidget("contents", "Value", input)
        if input == "close":
            break


      UI.CloseDialog()


DumbTab1Client().main()

