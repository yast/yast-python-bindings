# encoding: utf-8

# Advanced MultiSelectionBox example:
#
# Retrieve the list of selected items and output it.
from yast import import_module
import_module('UI')
from yast import *
class MultiSelectionBox3Client:
    def main(self):

      UI.OpenDialog(
        VBox(
          MultiSelectionBox(
            Id("toppings"),
            "Select pizza toppings:",
            [
              Item(Id("cheese"), "Cheese", True),
              Item(Id("tomatoes"), "Tomatoes", True),
              Item(Id("mush"), "Mushrooms", False),
              Item(Id("onions"), "Onions"),
              Item(Id("sausage"), "Salami"),
              Item(Id("pork"), "Ham")
            ]
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.ChangeWidget("toppings", "SelectedItems", ["sausage", "onions"])

      UI.UserInput()
      selected_items = UI.QueryWidget(Id("toppings"), "SelectedItems")

      ycpbuiltins.y2debug("Selected items: %1", selected_items)

      # Remember to retrieve the widget's data _before_ the dialog is closed,
      # i.e. before it is destroyed!

      UI.CloseDialog()



      # Concatenate the list of selected toppings to one multi-line string.

      pizza_description = ""

      for topping in ycpbuiltins.foreach(selected_items):
        pizza_description = ycpbuiltins.sformat(
          "%1\n%2",
          pizza_description,
          topping
        )


      # Open a new dialog to echo the selection.

      UI.OpenDialog(
        VBox(
          Label("Your pizza will come with:\n"),
          Label(pizza_description),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MultiSelectionBox3Client().main()

