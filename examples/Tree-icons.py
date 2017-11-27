# encoding: utf-8

# Tree with icons
from yast import *
class TreeIconsClient:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("YaST2 Mini Control Center"),
          Tree(
            Id("mod"),
            "Modules",
            [
              Item(
                Id("country"),
                Term("icon", "yast-language.png"),
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
              Item(
                Id("sw_single"),
                Term("icon", "yast-software.png"),
                "Software"
              )
            ]
          ),
          PushButton(Id("ok"), Opt("default"), "&OK")
        )
      )

      UI.UserInput()
      UI.CloseDialog()


TreeIconsClient().main()

