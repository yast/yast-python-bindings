# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Password2Client:
    def main(self):
      # Build dialog with two password fields, an "OK" and a "Cancel" button.
      UI.OpenDialog(
        VBox(
          Password(Id("pw1"), "Enter password:"),
          Password(Id("pw2"), "Confirm password:"),
          HBox(PushButton(Id("ok"), "&OK"), PushButton(Id("cancel"), "&Cancel"))
        )
      )
      button = None
      pw1 = ""
      pw2 = ""
      while True:
        # Wait for Input.
        button = UI.UserInput()

        # Get the values from both password fields.
        pw1 = UI.QueryWidget(Id("pw1"), "Value")
        pw2 = UI.QueryWidget(Id("pw2"), "Value")

        if button != "cancel":
          if pw1 == "" and pw2 == "":
            # Error popup if nothing has been entered.
            UI.OpenDialog(
              VBox(Label("You must enter a password."), PushButton("&OK"))
            )
            UI.UserInput()
            UI.CloseDialog()
          elif pw1 != pw2:
            # Error popup if passwords differ.
            UI.OpenDialog(
              VBox(
                Label("The two passwords mismatch."),
                Label("Please try again."),
                PushButton("&OK")
              )
            )
            UI.UserInput()
            UI.CloseDialog()
        if (pw1 != "" and pw1 == pw2) or button == "cancel":
          break

      UI.CloseDialog()


Password2Client().main()

