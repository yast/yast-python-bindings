# encoding: utf-8

# "Really Abort" pop-up dialog
from yast import import_module
import_module('UI')
from yast import *
class ReallyAbortPopupClient:
    def main(self):

      msg = "Really abort?\n" + "There are unsaved changes."

      content = VBox(
        VSpacing(0.3),
        HBox(
          Image(
            "/usr/share/YaST2/theme/current/icons/32x32/apps/msg_warning.png"
          ),
          Label(msg)
        ),
        VSpacing(0.3),
        ButtonBox(
          PushButton(Opt("okButton"), "&Discard Changes"),
          PushButton(Opt("cancelButton"), "&Back to Application")
        )
      )


      UI.OpenDialog(MarginBox(1, 0.1, VCenter(content)))
      UI.UserInput()
      UI.CloseDialog()


ReallyAbortPopupClient().main()

