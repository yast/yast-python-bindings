from __future__ import unicode_literals
# encoding: utf-8

# Table example: Exchange complete table content
from yast import import_module
import_module('UI')
from yast import *
class Table3Client:
    def main(self):
      foodItems = [
        Item(Id(3), "Spaghetti", 8),
        Item(Id(4), "Steak Sandwich", 12),
        Item(Id(1), "Chili", 6),
        Item(Id(2), "Salami Baguette", None)
      ]

      carItems = [
        Item(Id(0), "Mercedes", 60000),
        Item(Id(1), "Audi", 50000),
        Item(Id(2), "VW", 40000),
        Item(Id(3), "BMW", 60000),
        Item(Id(3), "Porsche", 80000)
      ]

      itemLists = [foodItems, carItems]

      listNo = 0

      UI.OpenDialog(
        VBox(
          Heading("Prices"),
          MinSize(
            30,
            10,
            Table(Id("table"), Header("Name", "Price"), foodItems)
          ),
          Right(
            HBox(
              PushButton(Id("next"), "Change &Table Contents"),
              PushButton(Id("cancel"), "&Close")
            )
          )
        )
      )

      while UI.UserInput() != "cancel":
        # Change table contents

        listNo = 1 - listNo
        UI.ChangeWidget("table", "Items", itemLists[listNo])

        # Double check: Retrieve contents and dump to log
        ycpbuiltins.y2milestone(
          "New table content:\n%1",
          UI.QueryWidget("table", "Items")
        )

      UI.CloseDialog()


Table3Client().main()

