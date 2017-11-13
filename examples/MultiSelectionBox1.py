# encoding: utf-8

from yast import *
class MultiSelectionBox1Client:
    def main(self):
      # Simple MultiSelectionBox example:
      #
      # All items are simple strings, none has an ID, no item preselected.

      UI.OpenDialog(
        VBox(
          MultiSelectionBox(
            "Select pizza toppings:",
            ["Cheese", "Tomatoes", "Mushrooms", "Onions", "Salami", "Ham"]
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


MultiSelectionBox1Client().main()

