# encoding: utf-8

from yast import *
class ShortcutConflict2Client:
    def main(self):
      # Demo for shortcut checking:
      # Deliberately generate a shortcut conflict.

      UI.OpenDialog(
        VBox(
          PushButton(Id(1), "&Do Something 1..."),
          PushButton(Id(2), "&Do Something 2..."),
          PushButton(Id(3), "&Do Something 3..."),
          PushButton(Id("quit"), "&Quit")
        )
      )


      button = None
      count = 3
      while True:
        button = UI.UserInput()

        if button != "quit":
          count = count + 1
          label = ycpbuiltins.sformat("&Do Something %1...", count)
          ycpbuiltins.y2milestone(
            "Changing button label for button #%1 to \"%2\"",
            button,
            label
          )
          UI.ChangeWidget(Id(button), "Label", label)
        if button == "quit":
          break


      UI.CloseDialog()


ShortcutConflict2Client().main()

