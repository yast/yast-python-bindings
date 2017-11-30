# encoding: utf-8

# Example showing how to replace Tree items
from yast import import_module
import_module('UI')
from yast import *
class TreeReplaceItemsClient:
    def main(self):

      pizza_list = [
        "Pizza Napoli",
        "Pizza Funghi",
        "Pizza Salami",
        "Pizza Hawaii"
      ]

      pasta_list = ["Spaghetti", "Rigatoni", "Tortellini"]

      veggie_toppings = [
        "Cheese",
        "Mushrooms",
        "Pepperoni",
        "Rucola",
        "Tomatoes"
      ]

      meat_toppings = ["Ham", "Salami", "Tuna"]

      menu = [
        Item(Id("pizza_branch"), "Pizza", True, pizza_list),
        Item(Id("pasta_branch"), "Pasta", True, pasta_list)
      ]

      toppings = [
        Item(Id("meat_branch"), "Meat", True, meat_toppings),
        Item(Id("veggie_branch"), "Veggie", True, veggie_toppings)
      ]


      UI.OpenDialog(
        VBox(
          Tree(Id("listing"), "Daily &Specials:", menu),
          HBox(
            PushButton(Id("menu"), "&Menu"),
            PushButton(Id("toppings"), "&Toppings"),
            PushButton(Id("empty"), "&None")
          ),
          PushButton(Id("ok"), "&OK")
        )
      )

      button = None
      while True:
        button = UI.UserInput()

        if button == "menu":
          UI.ChangeWidget("listing", "Items", menu)
        if button == "toppings":
          UI.ChangeWidget("listing", "Items", toppings)
        if button == "empty":
          UI.ChangeWidget("listing", "Items", [])
        if button == "ok":
          break

      order = UI.QueryWidget("listing", "CurrentItem")
      UI.CloseDialog()


      #
      # Show the result
      #

      UI.OpenDialog(
        VBox(
          Label(ycpbuiltins.sformat("Your order: %1", order)),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


TreeReplaceItemsClient().main()

