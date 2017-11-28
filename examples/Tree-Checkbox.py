# encoding: utf-8

# Tree with icons
from yast import import_module
import_module('UI')
from yast import *
class TreeCheckboxClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("YaST2 Mini Control Center"),
          Tree(
            Id("mod"),
            Opt("multiSelection"),
            "Modules",
            [
              Item(
                Id("country"),
                Term("icon", "yast-yast-language.png"),
                "Localization",
                True,
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
          PushButton(Id("ok"), Opt("default"), "&OK")
        )
      )

      UI.ChangeWidget("mod", "SelectedItems", [Id("xmas"), Id("newyear")])

      id = None
      while True:
        id = UI.TimeoutUserInput(300)
        selected_items = UI.QueryWidget(Id("mod"), "SelectedItems")

        ycpbuiltins.y2warning("Selected items: %1", selected_items)
        if id == "ok":
          break

      UI.CloseDialog()

TreeCheckboxClient().main()

