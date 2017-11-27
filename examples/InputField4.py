# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class InputField4Client:
    def main(self):
      # Build dialog with one input field field, 4 Beatles buttons and an OK button.
      UI.OpenDialog(
        VBox(
          InputField(Id("name"), "Name:"),
          HBox(
            PushButton(Id("john"), "&John"),
            PushButton(Id("paul"), "&Paul"),
            PushButton(Id("george"), "&George"),
            PushButton(Id("ringo"), "&Ringo")
          ),
          PushButton(Id("ok"), "&OK")
        )
      )

      # Wait for user input.
      button = None
      while True:
        button = UI.UserInput()

        if button == "john":
          UI.ChangeWidget(Id("name"), "Value", "John Lennon")
        elif button == "paul":
          UI.ChangeWidget(Id("name"), "Value", "Paul McCartney")
        elif button == "george":
          UI.ChangeWidget(Id("name"), "Value", "George Harrison")
        elif button == "ringo":
          UI.ChangeWidget(Id("name"), "Value", "Ringo Starr")
        if button == "ok":
          break

      UI.CloseDialog()


InputField4Client().main()

