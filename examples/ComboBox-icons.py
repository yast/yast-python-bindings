from __future__ import unicode_literals
# encoding: utf-8
from yast import import_module
import_module('UI')
from yast import *

# Combo box with icons
class ComboBoxIconsClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("YaST2 Mini Control Center"),
          ComboBox(
            Id("mod"),
            "Modules",
            [
              Item(Id("keyboard"), Term("icon", "yast-keyboard.png"), "Keyboard"),
              Item(Id("mouse"), Term("icon", "yast-mouse.png"), "Mouse"),
              Item(
                Id("timezone"),
                Term("icon", "yast-timezone.png"),
                "Time zone"
              ),
              Item(Id("lan"), Term("icon", "yast-lan.png"), "Network"),
              Item(
                Id("sw_single"),
                Term("icon", "yast-software.png"),
                "Software"
              )
            ]
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()

      # Get the input from the combo box.
      #
      # Notice: The return value of UI::UserInput() does NOT return this value!
      # Rather, it returns the ID of the widget (normally the PushButton)
      # that caused UI::UserInput() to return.
      mod = UI.QueryWidget(Id("mod"), "Value")

      # Close the dialog.
      # Remember to read values from the dialog's widgets BEFORE closing it!
      UI.CloseDialog()

ComboBoxIconsClient().main()
