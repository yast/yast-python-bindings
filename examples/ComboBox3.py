# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

# Create a combo box with three entries.
# All entries have IDs to identify them independent of locale
# (The texts might have to be translated!).
# Entry "Funghi" will be selected by default.
class ComboBox3Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          ComboBox(
            Id("pizza"),
            Opt("editable"),
            "Select your Pizza:",
            [
              Item(Id("nap"), "Napoli"),
              Item(Id("fun"), "Funghi", True),
              Item(Id("sal"), "Salami")
            ]
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()

      # Get the input from the selection box.
      #
      # Notice: The return value of UI::UserInput() does NOT return this value!
      # Rather, it returns the ID of the widget (normally the PushButton)
      # that caused UI::UserInput() to return.
      pizza = UI.QueryWidget(Id("pizza"), "Value")
      ycpbuiltins.y2milestone("Selected %1", pizza)

      # Close the dialog.
      # Remember to read values from the dialog's widgets BEFORE closing it!
      UI.CloseDialog()

      # Evaluate selection

      toppings = "nothing"

      if pizza == "nap":
        toppings = "Tomatoes, Cheese"
      elif pizza == "fun":
        toppings = "Tomatoes, Cheese, Mushrooms"
      elif pizza == "sal":
        toppings = "Tomatoes, Cheese, Sausage"

      # Pop up a new dialog to echo the selection.
      UI.OpenDialog(
        VBox(
          Label("You will get a pizza with:"),
          Label(toppings),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()

ComboBox3Client().main()
