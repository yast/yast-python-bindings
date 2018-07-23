from __future__ import unicode_literals
# encoding: utf-8

# Example of using the Wizard widget.
#
# Note: YCP applications are discouraged from using the Wizard widget directly.
# Use the Wizard module instead.
from yast import import_module
import_module('UI')
from yast import *
class WizardPopupClient:
    def main(self):
      if not UI.HasSpecialWidget("Wizard"):
        ycpbuiltins.y2error(
          "This works only with UIs that provide the wizard widget!"
        )
        return

      help_text = "<p>This is a help text.</p>" + "<p>It should be helpful.</p>" + "<p>If it isn't helpful, it should rather not be called a <i>help text</i>.</p>"

      UI.OpenDialog(
        Opt("defaultsize"),
        Wizard(
          Opt("stepsEnabled"),
          Symbol("back"),
          "&Back",
          Symbol("abort"),
          "Ab&ort",
          Symbol("next"),
          "&Next"
        )
      )

      # UI::DumpWidgetTree();

      UI.WizardCommand(
        Term(
          "SetDialogIcon",
          "/usr/share/YaST2/theme/current/icons/22x22/apps/YaST.png"
        )
      )
      UI.WizardCommand(Term("SetDialogHeading", "Wizard with Pop-up Wizard"))
      UI.WizardCommand(Term("SetHelpText", help_text))

      UI.WizardCommand(Term("AddStepHeading", "Steps"))
      UI.WizardCommand(Term("AddStep", "Step 1", "step1"))
      UI.WizardCommand(Term("AddStep", "Step 2", "step2"))
      UI.WizardCommand(Term("AddStep", "Step 3", "step3"))

      UI.WizardCommand(Term("UpdateSteps"))

      UI.ReplaceWidget(
        "contents",
        VBox(
          PushButton(Id("doit1"), "&Do Something"),
          PushButton(Id("doit2"), "Do &More"),
          PushButton(Id("popup"), "Popup &Wizard")
        )
      )

      UI.WizardCommand(Term("SetCurrentStep", "step1"))


      while True:
        event = UI.WaitForEvent()

        ycpbuiltins.y2milestone("Got event: %1", event)

        widget = event["ID"]

        if widget == "abort":
          break

        if widget == "popup":
          UI.OpenDialog(
            Opt("defaultsize"),
            Wizard(Symbol("bla"), "", Symbol("popdown"), "&Cancel", Symbol("accept"), "&Acce&pt")
          )

          UI.ReplaceWidget(
            "contents",
            VBox(
              Id("popupWizard"),
              Heading("Popup Wizard"),
              VSpacing(2),
              PushButton(Id("doit11"), "&Do Something"),
              PushButton(Id("doit12"), "Do &More")
            )
          )

        if widget == "popdown" and UI.WidgetExists("popupWizard"):
          UI.CloseDialog()

      UI.CloseDialog()


WizardPopupClient().main()

