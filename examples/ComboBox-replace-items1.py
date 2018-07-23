from __future__ import unicode_literals
# encoding: utf-8
from yast import import_module
import_module('UI')
from yast import *

# Example showing how to replace SelectionBox items
class ComboBoxReplaceItems1Client:
    def main(self):

      pizza_list = [
        "Pizza Napoli",
        "Pizza Funghi",
        "Pizza Salami",
        "Pizza Hawaii"
      ]

      pasta_list = ["Spaghetti", "Rigatoni", "Tortellini"]

      UI.OpenDialog(
        VBox(
          ComboBox(Id("menu"), "Daily &Specials:", pizza_list),
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

      order = UI.QueryWidget("menu", "Value")
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

ComboBoxReplaceItems1Client().main()
