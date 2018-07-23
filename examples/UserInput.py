from __future__ import unicode_literals
# encoding: utf-8

# UserInput.ycp
#
# Example for common usage of UI::UserInput()
from yast import import_module
import_module('UI')
from yast import *
class UserInputClient:
    def main(self):
      # Build dialog with two input fields and three buttons.
      #
      # Output goes to the log file: ~/.y2log for normal users
      # or /var/log/YaST2/y2log for root.

      name = "Tux"
      addr = "Antarctica"

      UI.OpenDialog(
        VBox(
          InputField(Id("name"), "&Name:", name),
          InputField(Id("addr"), "&Address:", addr),
          HBox(
            PushButton(Id("ok"), "&OK"),
            PushButton(Id("cancel"), "&Cancel"),
            PushButton(Id("help"), "&Help")
          )
        )
      )

      widget_id = None
      while True:
        widget_id = UI.UserInput()

        if widget_id == "ok":
          # process "OK" button

          ycpbuiltins.y2milestone("OK button activated")


          # Retrieve widget contents

          name = UI.QueryWidget(Id("name"), "Value")
          addr = UI.QueryWidget(Id("addr"), "Value")
        elif widget_id == "cancel":
          # process "Cancel" buttton
          # or window manager close button (this also returns `cancel)

          ycpbuiltins.y2milestone("Cancel button activated")
        elif widget_id == "help":
          # process "Help" button

          ycpbuiltins.y2milestone("Help button activated")

        # No other "else:" branch necessary: None of the InputField widget has
        # the `notify option set, so none of them can make UI::UserInput() return.
        if widget_id == "ok" or widget_id == "cancel":
          break



      # Close the dialog - but only after retrieving all information that may
      # still be stored only in its widgets: UI::QueryWidget() works only for
      # widgets that are still on the screen!

      UI.CloseDialog()


      # Dump the values entered into the log file

      ycpbuiltins.y2milestone("Name: %1 Address: %2", name, addr)


UserInputClient().main()

