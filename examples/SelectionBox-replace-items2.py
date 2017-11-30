# encoding: utf-8

# Example showing how to replace SelectionBox items
from yast import import_module
import_module('UI')
from yast import *
class SelectionBoxReplaceItems2Client:
    def main(self):

      pizza_list = [
        Item(Id("Pizza #01"), "Pizza Napoli"),
        Item(Id("Pizza #02"), "Pizza Funghi"),
        Item(Id("Pizza #03"), "Pizza Salami", True),
        Item(Id("Pizza #04"), "Pizza Hawaii")
      ]

      pasta_list = [
        Item(Id("Pasta #11"), "Spaghetti"),
        Item(Id("Pasta #12"), "Rigatoni", True),
        Item(Id("Pasta #13"), "Tortellini")
      ]

      UI.OpenDialog(
        VBox(
          SelectionBox(Id("menu"), "Daily &Specials:", pizza_list),
          HBox(
            PushButton(Id("pizza"), "Pi&zza"),
            PushButton(Id("pasta"), "&Pasta")
          ),
          PushButton(Id("ok"), "&OK")
        )
      )

      button = None
      while True:
        button = UI.UserInput()

        if button == "pizza":
          UI.ChangeWidget("menu", "Items", pizza_list)
        if button == "pasta":
          UI.ChangeWidget("menu", "Items", pasta_list)
        if button == "ok":
          break

      order = UI.QueryWidget("menu", "CurrentItem")
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


SelectionBoxReplaceItems2Client().main()

