# encoding: utf-8

# Tree with recursive multi selection
from yast import import_module
import_module('UI')
from yast import *
import copy

class TreeCheckbox4Client:
    def main(self):



      UI.OpenDialog(
        MinSize( 40, 15,
          VBox(
            Heading("YaST2 Mini Control Center"),
            Tree(
              Id("mod"),
              Opt("multiSelection", "notify", "immediate", "recursiveSelection"),
              "Modules",
              [
                Item(Id("unselected"), "Unseleted"),
                Item(
                  Id("country"),
                  "Localization",
                  True,
                  [
                    Item(Id("keyboard"), "Keyboard"),
                    Item(
                      Id("timezone"),
                      "Time zone",
                      True,
                      [Item(Id("europe"), "Europe"), Item(Id("asia"), "Asia")]
                    )
                  ]
                ),
                Item(Id("mouse"), "Mouse"),
                Item(Id("lan"), "Network"),
                Item(Id("xmas"), "Merry X-Mas"),
                Item(Id("newyear"), "Happy New Year")
              ]
            ),
            PushButton(Id("ok"), Opt("default"), "&OK")
          )
        )
      )

      UI.ChangeWidget("mod", "SelectedItems", [Symbol("lan"), Symbol("mouse")])
      UI.ChangeWidget("mod", "SelectedItems", [Symbol("xmas"), Symbol("newyear")])

      selected_items = UI.QueryWidget(Id("mod"), "SelectedItems")

      ycpbuiltins.y2warning("Selected items: %1", selected_items)


      id = None

      event = {}
      while True:
        event = UI.WaitForEvent(1000 * 100)

        if event["EventReason"] == "SelectionChanged":
          ycpbuiltins.y2error("Selection Changed Event")

        if event["EventReason"] == "ValueChanged":
          ycpbuiltins.y2error("Value Changed Event")

        if event["EventType"] == "TimeoutEvent":
          ycpbuiltins.y2error("Timeout Event")

        if event != None:
          ycpbuiltins.y2error(self.formatEvent(event))

        id = event["ID"]
        ycpbuiltins.y2milestone(
          "Selected items: %1",
          UI.QueryWidget(Id("mod"), "SelectedItems"))

        if id == "ok":
          break
      UI.CloseDialog()

    def formatEvent(self, event):
      event = copy.deepcopy(event)
      html = "Event:"
      for key, value in ycpbuiltins.foreach(event).items():
        html = html +  " " +  key + ": " + ycpbuiltins.tostring(value) + ""

      return html

TreeCheckbox4Client().main()

