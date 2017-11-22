# encoding: utf-8

from yast import *
class MultiSelectionBox2Client:
    def main(self):
      # More realistic MultiSelectionBox example:
      #
      # Items have IDs, some are preselected.
      # Notice 'False' is default anyway for the selection state,
      # so you may or may not explicitly specify that.

      UI.OpenDialog(
        VBox(
          MultiSelectionBox(
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
      UI.UserInput()
      UI.CloseDialog()


MultiSelectionBox2Client().main()

