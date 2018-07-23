from __future__ import unicode_literals
# encoding: utf-8
import copy
from yast import import_module
import_module('UI')
from yast import *
class Table8MultiSelClient:
    def main(self):
      new_items = [
        Item(Id(1), "Mercedes", 60000),
        Item(Id(2), "Audi", 50000),
        Item(Id(3), "VW", 40000),
        Item(Id(4), "BMW", 60000),
        Item(Id(5), "Porsche", 80000)
      ]
      orig_items = [
        Item(Id(1), "Chili", 6),
        Item(Id(2), "Salami Baguette", None),
        Item(Id(3), "Spaghetti", 8),
        Item(Id(4), "Steak Sandwich", 12)
      ]

      UI.OpenDialog(
        VBox(
          Heading("Today's menu"),
          MinSize(
            30,
            10,
            Table(
              Id("menu"),
              Opt("notify", "multiSelection"),
              Header("Name", "Price"),
              [
                Item(Id(1), "Chili", 6),
                Item(Id(2), "Salami Baguette", None),
                Item(Id(3), "Spaghetti", 8),
                Item(Id(4), "Steak Sandwich", 12)
              ]
            )
          ),
          Label("Get notified on 'Return' or double click"),
          HBox(Label("Selected: "), TextEntry(Id("info"), "")),
          HBox(
            PushButton(Id("next"), "Change &Table Contents"),
            PushButton(Id("cancel"), "&OK")
          )
        )
      )

      UI.ChangeWidget("menu", "SelectedItems", [1, 2])
      sel = UI.QueryWidget("menu", "SelectedItems")

      selItems = ""
      for val in ycpbuiltins.foreach(sel):
        selItems = selItems + " " + str(val)

      UI.ChangeWidget("info", "Value", selItems)

      event = {}
      num = 0
      while True:
        selItems2 = ""
        event = UI.WaitForEvent()

        if event["ID"] == "menu":
          sel = UI.QueryWidget("menu", "SelectedItems")
          for val in ycpbuiltins.foreach(sel):
            selItems2 = selItems2 + " " + str(val)
          UI.ChangeWidget("info", "Value", selItems2)

        elif event["ID"] == "next":
          num = num + 1
          items = []
          if num % 2 == 1:
            #items = copy.deepcopy(new_items)
            items = new_items
          else:
            #items = copy.deepcopy(orig_items)
            items = orig_items

          # Change table contents
          UI.ChangeWidget("menu", "Items", items)
          sel = UI.QueryWidget("menu", "SelectedItems")

          for val in ycpbuiltins.foreach(sel):
            selItems2 = selItems2 + " " + val

          UI.ChangeWidget("info", "Value", selItems2)

          # Double check: Retrieve contents and dump to log
          ycpbuiltins.y2milestone(
            "New table content:\n%1",
            UI.QueryWidget("menu", "Items")
          )
        if event["ID"] == "cancel":
          break

      sel = UI.QueryWidget("menu", "SelectedItems")
      ycpbuiltins.y2milestone("Selected: %1", sel)

      UI.CloseDialog()


Table8MultiSelClient().main()

