# encoding: utf-8

from yast import *
class PushButton2Client:
    def main(self):
      # Build dialog with three buttons.
      # "Cancel" is the default button, i.e. pressing "Return" will
      # activate it.

      UI.OpenDialog(
        HBox(
          PushButton(Id("ok"), "&OK"),
          PushButton(Id("cancel"), Opt("default"), "&Cancel"),
          PushButton(Id("help"), "&Help")
        )
      )

      # Wait for user input. The value returned is the ID of the widget
      # that makes UI::UserInput() terminate, i.e. the respective button ID.
      button_id = UI.UserInput()

      # Close the dialog.
      UI.CloseDialog()


      # Process the input.
      button_name = ""
      if button_id == "ok":
        button_name = "OK"
      elif button_id == "cancel":
        button_name = "Cancel"
      elif button_id == "help":
        button_name = "Help"

      # Pop up a new dialog to display what button was clicked.
      UI.OpenDialog(
        VBox(
          Label("You clicked button \"" + button_name + "\"."),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


PushButton2Client().main()

