# encoding: utf-8

# Example showing how to replace SelectionBox items
from yast import *
class MultiSelectionBoxReplaceItems1Client:
    def main(self):

      all_toppings = [
        "Cheese",
        "Ham",
        "Mushrooms",
        "Pepperoni",
        "Rucola",
        "Salami",
        "Tomatoes",
        "Tuna"
      ]

      veggie_toppings = [
        "Cheese",
        "Mushrooms",
        "Pepperoni",
        "Rucola",
        "Tomatoes"
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


MultiSelectionBoxReplaceItems1Client().main()

