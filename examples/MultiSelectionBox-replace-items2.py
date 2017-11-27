# encoding: utf-8

# Example showing how to replace SelectionBox items
from yast import import_module
import_module('UI')
from yast import *
class MultiSelectionBoxReplaceItems2Client:
    def main(self):

      all_toppings = [
        Item(Id("Cheese"), "Cheese", True),
        Item(Id("Tomatoes"), "Tomatoes", True),
        Item(Id("Ham"), "Ham"),
        Item(Id("Mushrooms"), "Mushrooms"),
        Item(Id("Pepperoni"), "Pepperoni"),
        Item(Id("Rucola"), "Rucola"),
        Item(Id("Salami"), "Salami"),
        Item(Id("Tuna"), "Tuna")
      ]

      veggie_toppings = [
        Item(Id("Cheese"), "Cheese", True),
        Item(Id("Tomatoes"), "Tomatoes", True),
        Item(Id("Mushrooms"), "Mushrooms"),
        Item(Id("Pepperoni"), "Pepperoni"),
        Item(Id("Rucola"), "Rucola")
      ]

      UI.OpenDialog(
        HBox(
          VSpacing(15), # layout trick: force minimum height
          VBox(
            HSpacing(25), # force minimum width
            MultiSelectionBox(Id("toppings"), "Toppings:", all_toppings),
            Left(CheckBox(Id("veggie"), Opt("notify"), "&Vegetarian")),
            PushButton(Id("ok"), "&OK")
          )
        )
      )

      button = None
      while True:
        button = UI.UserInput()

        if button == "veggie":
          vegetarian = UI.QueryWidget("veggie", "Value")

          if vegetarian:
            UI.ChangeWidget("toppings", "Items", veggie_toppings)
          else:
            UI.ChangeWidget("toppings", "Items", all_toppings)
        if button == "ok":
          break

      order = UI.QueryWidget("toppings", "SelectedItems")
      UI.CloseDialog()


      #
      # Show the result
      #


      UI.OpenDialog(
        VBox(
          Label(
            ycpbuiltins.sformat(
              "Your order: %1",
              ycpbuiltins.mergestring(order, ", ")
            )
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MultiSelectionBoxReplaceItems2Client().main()

