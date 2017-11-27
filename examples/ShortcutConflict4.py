# encoding: utf-8

# Demo for shortcut checking:
# Deliberately generate a shortcut conflict.
#
# This kind of conflict cannot be resolved.
# Only one of the Widgets with "&A" will get a shortcut at all.
from yast import *
class ShortcutConflict4Client:
    def main(self):


      UI.OpenDialog(
        VBox(
          PushButton(Id(1), "&A"),
          PushButton(Id(2), "&A"),
          PushButton(Id(3), "&A"),
          PushButton(Id("quit"), "&Quit")
        )
      )


      button = None
      while True:
        button = UI.UserInput()
        if button == "quit":
          break


      UI.CloseDialog()


ShortcutConflict4Client().main()

