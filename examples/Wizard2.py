# encoding: utf-8

# Example of using the Wizard widget.
#
# Note: YCP applications are discouraged from using the Wizard widget directly.
# Use the Wizard module instead.
from yast import import_module
import_module('UI')
from yast import *
class Wizard2Client:
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
      UI.WizardCommand(
        Term("SetDialogHeading", "Welcome to the YaST2 installation")
      )
      UI.WizardCommand(Term("SetHelpText", help_text))

      UI.WizardCommand(Term("AddStepHeading", "Base Installation"))
      UI.WizardCommand(Term("AddStep", "Language", "lang"))
      UI.WizardCommand(Term("AddStep", "Installation Settings", "proposal"))
      UI.WizardCommand(Term("AddStep", "Perform Installation", "doit"))

      UI.WizardCommand(Term("AddStepHeading", "Configuration"))
      UI.WizardCommand(Term("AddStep", "Root Password", "root_pw"))
      UI.WizardCommand(Term("AddStep", "Network", "net"))
      UI.WizardCommand(Term("AddStep", "Online Update", "you"))
      UI.WizardCommand(Term("AddStep", "Users", "auth"))
      UI.WizardCommand(Term("AddStep", "Clean Up", "suse_config"))
      UI.WizardCommand(Term("AddStep", "Release Notes", "rel_notes"))
      UI.WizardCommand(Term("AddStep", "Device Configuration", "hw_proposal"))
      UI.WizardCommand(Term("UpdateSteps"))

      if False:
        UI.WizardCommand(Term("SetAbortButtonLabel", "&Cancel"))
        UI.WizardCommand(Term("SetBackButtonLabel", ""))
        UI.WizardCommand(Term("SetNextButtonLabel", "&Accept"))

      UI.WizardCommand(Term("SetCurrentStep", "net"))

      while True:
        event = UI.WaitForEvent()

        ycpbuiltins.y2milestone("Got event: %1", event)

        if event["ID"] == "abort":
          break

        serial = event["EventSerialNo"]
        type = event["EventType"]
        id = event["ID"]


        UI.ReplaceWidget(
          Id("contents"),
          VBox(
            Heading("Caught event:"),
            VSpacing(0.5),
            Label("Serial No: " + str(serial)),
            Label("Type: " + type),
            Label("ID: " + id)))

      UI.CloseDialog()


Wizard2Client().main()

