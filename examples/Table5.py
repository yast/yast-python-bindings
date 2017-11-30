# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Table5Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MinSize(
            25,
            8,
            Table(
              Id("table"),
              Opt("notify"),
              Header("Name", "Amount"),
              [
                Item(Id(1), "Chili", 0),
                Item(Id(2), "Salami Baguette", 0),
                Item(Id(3), "Spaghetti", 0),
                Item(Id(4), "Steak Sandwich", 0)
              ]
            )
          ),
          Label("Double-click any item to increase the number"),
          Right(PushButton(Id("cancel"), "&Close"))
        )
      )

      while UI.UserInput() != "cancel":
        current_item_id = int(UI.QueryWidget(Id("table"), "CurrentItem"))
        amount = int(UI.QueryWidget("table", Cell(current_item_id, 1)))
        amount = amount + 1
        ycpbuiltins.y2debug("amount: %1", amount)
        UI.ChangeWidget(Id("table"), Cell(current_item_id, 1), amount)

      UI.CloseDialog()


Table5Client().main()

