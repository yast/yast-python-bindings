# encoding: utf-8

# Advanced MultiSelectionBox example:
#
# Get and change the current item. Note that unlike with a SelectionBox, this
# is typically NOT what an application needs: The current item is the item
# that has the keyboard focus. It doesn't need to be selected. Most
# applications will want to use SelectedItems rather than CurrentItem.
from yast import import_module
import_module('UI')
from yast import *
class MultiSelectionBoxCurrentItemClient:
    def main(self):

      UI.OpenDialog(
        VBox(
          MultiSelectionBox(
            Id("toppings"),
            "Select pizza toppings:",
            [
              Item(Id(0), "Cheese", True),
              Item(Id(1), "Tomatoes", True),
              Item(Id(2), "Mushrooms", False),
              Item(Id(3), "Onions"),
              Item(Id(4), "Salami"),
              Item(Id(5), "Ham")
            ]
          ),
          HBox(
            PushButton(Id("next"), "&Next"),
            HStretch(),
            PushButton(Id("cancel"), "&Close")
          )
        )
      )

      widget = None
      while True:
        widget = UI.UserInput()

        if widget == "next":
          current = int(UI.QueryWidget("toppings", "CurrentItem"))

          current = current + 1
          if current > 5:
            current = 0

          ycpbuiltins.y2milestone("Current: %1", current)
          UI.ChangeWidget("toppings", "CurrentItem", current)
        if widget == "cancel":
          break     

      UI.CloseDialog()


MultiSelectionBoxCurrentItemClient().main()

