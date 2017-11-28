# encoding: utf-8

# Shortcut conflict resolution in a (really badly designed) wizard dialog.
#
# Notice how wizard buttons have overall priority and how buttons
# have priority over other widgets of the same length.
#
# Note: YCP applications are discouraged from using the Wizard widget directly.
# Use the Wizard module instead.
from yast import import_module
import_module('UI')
from yast import *
class ShortcutConflict5Client:
    def main(self):
      UI.OpenDialog(
        Opt("defaultsize"),
        Wizard("back", "&Back", "abort", "&Abort", "next", "&Next")
      )

      fields = HBox(
        HWeight(1, InputField("&Back")),
        HWeight(1, InputField("&Abort")),
        HWeight(1, InputField("&Next"))
      )

      buttons = HBox(
        HWeight(1, PushButton("&Back")),
        HWeight(1, PushButton("&Abort")),
        HWeight(1, PushButton("&Next"))
      )

      UI.ReplaceWidget(Id("contents"), VBox(fields, fields, buttons))

      help_text = "Notice how the wizard buttons keep their preferred shortcuts " + "and how buttons have priority over other widgets."

      UI.WizardCommand(Term("SetHelpText", help_text))

      while True:
        event = UI.WaitForEvent()

        ycpbuiltins.y2milestone("Got event: %1", event)

        if Ops.get(event, "ID") == "abort":
          break

      UI.CloseDialog()


ShortcutConflict5Client().main()

