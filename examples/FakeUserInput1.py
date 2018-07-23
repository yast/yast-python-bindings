from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class FakeUserInput1Client:
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

      UI.FakeUserInput("john")
      UI.FakeUserInput("paul")
      UI.FakeUserInput("george")
      UI.FakeUserInput("ringo")
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

        ycpbuiltins.sleep(3 * 1000)
        if button == "ok":
            break

      UI.CloseDialog()


FakeUserInput1Client().main()

