# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Table2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("Today's menu"),
          MinSize(
            30,
            7,
            Table(
              Id("table"),
              Opt("keepSorting"),
              Header("Name", Right("Price"), Center("Rating")),
              [
                Item(Id(0), "Steak Sandwich", 12, "+++"),
                Item(Id(1), "Salami Baguette", None, "-"),
                Item(Id(2), "Chili", 6, "--"),
                Item(Id(3), "Spaghetti", 8, "+")
              ]
            )
          ),
          Right(
            HBox(
              PushButton(Id("next"), "&Next"),
              PushButton(Id("cancel"), "&Close")
            )
          )
        )
      )

      UI.ChangeWidget(Id("table"), "CurrentItem", 2)

      while UI.UserInput() != "cancel":
        UI.ChangeWidget(
          Id("table"),
          "CurrentItem",
          ((UI.QueryWidget(Id("table"), "CurrentItem") + 1) % 4)
         )

      UI.CloseDialog()


Table2Client().main()

