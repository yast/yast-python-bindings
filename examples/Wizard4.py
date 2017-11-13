# encoding: utf-8

# Advanced example of using the Wizard widget.
#
# Note: YCP applications are discouraged from using the Wizard widget directly.
# Use the Wizard module instead.
from yast import *
class Wizard4Client:
    def main(self):
      if not UI.HasSpecialWidget("Wizard"):
        ycpbuiltins.y2error(
          "This works only with UIs that provide the wizard widget!"
        )
        return

      help_text = "<p>This is a help text.</p>" + "<p>It should be helpful.</p>" + "<p>If it isn't helpful, it should rather not be called a <i>help text</i>.</p>"

      UI.OpenDialog(
        Opt("defaultsize"),
        YCPWizard(
          Opt("treeEnabled"),
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


      UI.WizardCommand(Term("AddTreeItem", "", "First Toplevel Item", "tl1"))
      UI.WizardCommand(Term("AddTreeItem", "", "Second Toplevel Item", "tl2"))
      UI.WizardCommand(Term("AddTreeItem", "", "Third Toplevel Item", "tl3"))

      UI.WizardCommand(Term("AddTreeItem", "tl1", "First Sublevel", "1-1"))
      UI.WizardCommand(Term("AddTreeItem", "tl1", "Second Sublevel", "1-2"))
      UI.WizardCommand(Term("AddTreeItem", "tl1", "Third Sublevel", "1-3"))

      UI.WizardCommand(Term("AddTreeItem", "tl2", "First Sublevel", "2-1"))
      UI.WizardCommand(Term("AddTreeItem", "tl2", "Second Sublevel", "2-2"))
      UI.WizardCommand(Term("AddTreeItem", "tl2", "Third Sublevel", "2-3"))

      UI.WizardCommand(Term("AddTreeItem", "1-2", "First 3rd level ", "3rd 1"))
      UI.WizardCommand(Term("AddTreeItem", "1-2", "Second 3rd level ", "3rd 2"))
      UI.WizardCommand(Term("AddTreeItem", "1-2", "Item without ID", ""))

      UI.WizardCommand(Term("SelectTreeItem", "3rd 1"))



      UI.WizardCommand(Term("AddMenu", "&File", "file-menu"))
      UI.WizardCommand(Term("AddMenu", "&Edit", "edit-menu"))
      UI.WizardCommand(Term("AddMenu", "&Options", "opt-menu"))

      UI.WizardCommand(Term("AddMenuEntry", "file-menu", "&New", "file-new"))
      UI.WizardCommand(Term("AddMenuEntry", "file-menu", "&Open", "file-open"))
      UI.WizardCommand(
        Term("AddSubMenu", "file-menu", "Open &Recent", "file-recent")
      )
      UI.WizardCommand(Term("AddMenuEntry", "file-menu", "&Save", "file-save"))
      UI.WizardCommand(
        Term("AddMenuEntry", "file-menu", "Save &As", "file-save-as")
      )

      UI.WizardCommand(
        Term("AddMenuEntry", "file-recent", "/tmp/test1", "recent-test1")
      )
      UI.WizardCommand(
        Term("AddMenuEntry", "file-recent", "/tmp/test2", "recent-test2")
      )

      UI.WizardCommand(Term("AddMenuEntry", "edit-menu", "C&ut", "edit-cut"))
      UI.WizardCommand(Term("AddMenuEntry", "edit-menu", "C&opy", "edit-copy"))
      UI.WizardCommand(Term("AddMenuEntry", "edit-menu", "&Paste", "edit-paste"))

      UI.WizardCommand(
        Term("AddMenuEntry", "opt-menu", "&Settings", "opt-settings")
      )
      UI.WizardCommand(Term("AddMenuSeparator", "opt-menu"))
      UI.WizardCommand(
        Term(
          "AddMenuEntry",
          "opt-menu",
          "Activate &Hypersonic Transducer",
          "frank-n-furter"
        )
      )



      while True:
        event = UI.WaitForEvent()

        ycpbuiltins.y2milestone("Got event: %1", event)

        if event["ID"] == "abort":
          break

        ycpbuiltins.y2milestone(
          "Tree selection: %1",
          UI.QueryWidget(Id("wizard"), "CurrentItem")
        )

      UI.CloseDialog()


Wizard4Client().main()

