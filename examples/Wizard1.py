# encoding: utf-8

# Basic example of using the Wizard widget.
#
# Note: YCP applications are discouraged from using the Wizard widget directly.
# Use the Wizard module instead.
from yast import *
class Wizard1Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        YCPWizard(Symbol("back"), "", Symbol("abort"), "&Cancel", Symbol("next"), "&OK")
      )

      while True:
        event = UI.WaitForEvent()

        ycpbuiltins.y2milestone("Got event: %1", event)

        if event["ID"] == "abort":
          break

      UI.DumpWidgetTree()
      UI.CloseDialog()


Wizard1Client().main()

