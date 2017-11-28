# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Table7MultiSelClient:
    def main(self):
      new_items = [
        Item(Id(1), "Mercedes", 60000),
        Item(Id(2), "Audi", 50000),
        Item(Id(3), "VW", 40000),
        Item(Id(4), "BMW", 60000),
        Item(Id(5), "Porsche", 80000)
      ]

      UI.OpenDialog(
        VBox(
          Heading("Today's menu"),
          MinSize(
            30,
            10,
            Table(
              Id("menu"),
              Opt("multiSelection"),
              Header("Name", "Price"),
              [
                Item(Id(1), "Chili", 6),
                Item(Id(2), "Salami Baguette", None),
                Item(Id(3), "Spaghetti", 8),
                Item(Id(4), "Steak Sandwich", 12)
              ]
            )
          ),
          HBox(
            PushButton(Id("next"), "Change &Table Contents"),
            PushButton(Id("cancel"), "&OK")
          )
        )
      )

      UI.ChangeWidget("menu", "SelectedItems", [1,2])


      while UI.UserInput() != "cancel":
        # Change table contents
        UI.ChangeWidget("menu", "Items", new_items)

        # Double check: Retrieve contents and dump to log
        ycpbuiltins.y2milestone(
          "New table content:\n%1",
          UI.QueryWidget("menu", "Items")
        )
      sel = UI.QueryWidget("menu", "SelectedItems")
      UI.CloseDialog()

      ycpbuiltins.y2milestone("Selected: %1", sel)


Table7MultiSelClient().main()

