# encoding: utf-8

# Tree with icons
from yast import import_module
import_module('UI')
from yast import *
class TreeCheckbox2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("YaST2 Mini Control Center"),
          Tree(
            Id("mod"),
            Opt("notify", "multiSelection", "immediate"),
            "Modules",
            [
              Item(
                Id("country"),
                Term("icon", "yast-yast-language.png"),
                "Localization",
                False,
                [
                  Item(
                    Id("keyboard"),
                    Term("icon", "yast-keyboard.png"),
                    "Keyboard"
                  ),
                  Item(
                    Id("timezone"),
                    Term("icon", "yast-timezone.png"),
                    "Time zone"
                  )
                ]
              ),
              Item(Id("mouse"), Term("icon", "yast-mouse.png"), "Mouse"),
              Item(Id("lan"), Term("icon", "yast-lan.png"), "Network"),
              Item(Id("xmas"), Term("icon", "yast-software.png"), "Merry X-Mas"),
              Item(
                Id("newyear"),
                Term("icon", "yast-software.png"),
                "Happy New Year"
              )
            ]
          ),
          HBox(
            PushButton(Id("ok"), Opt("default"), "&OK"),
            PushButton(Id("deselect"), "&Log selected")
          )
        )
      )

      UI.ChangeWidget("mod", "SelectedItems", [Id("keyboard"), Id("xmas"), Id("newyear")])
      id = None
      current = UI.QueryWidget(Id("mod"), "CurrentItem")
      ycpbuiltins.y2milestone("Current item: %1", current)
      while True:
        id = UI.UserInput()
        selected_items = UI.QueryWidget(Id("mod"), "SelectedItems")

        ycpbuiltins.y2milestone("Selected items: %1", selected_items)
        current = UI.QueryWidget(Id("mod"), "CurrentItem")
        ycpbuiltins.y2milestone("Current item: %1", current)
        if id == "ok":
          break


TreeCheckbox2Client().main()

