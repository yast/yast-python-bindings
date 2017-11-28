# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

def is_int(val):
   try:
       int(val)
   except:
       return False
   return True

class Table4Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("Today's menu"),
          MinSize(
            25,
            7,
            Table(
              Id("table"),
              Header("Name", "Price"),
              [
                Item(Id(1), "Chili", 6),
                Item(Id(2), "Salami Baguette", None),
                Item(Id(3), "Spaghetti", 8),
                Item(Id(4), "Steak Sandwich", 12)
              ]
            )
          ),
          Right(HBox(PushButton("&Lookup"), PushButton(Id("cancel"), "&Close")))
        )
      )

      while UI.UserInput() != "cancel":
        id = UI.QueryWidget(Id("table"), "CurrentItem")
        if is_int(id):
          text = ycpbuiltins.sformat(
            "Line: %1",
            UI.QueryWidget(Id("table"), Term("Item", id))
          )
          UI.OpenDialog(
            MarginBox(
              1,
              0.2,
              VBox(
                Left(Label("Current Table Item")),
                Label(Opt("outputField"), text),
                PushButton("&OK")
              )
            )
          )
          UI.UserInput()
          UI.CloseDialog()

      UI.CloseDialog()


Table4Client().main()

