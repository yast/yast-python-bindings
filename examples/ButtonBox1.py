# encoding: utf-8

# Example for ButtonBox

from yast import *

class ButtonBox1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          HVCenter(Label("Hello, world!")),
          ButtonBox(
            PushButton(Id("doit1"), "Do &Something Very Cool"),
            PushButton(Id("doit2"), Opt("key_F10", "customButton"), "Do &More"),
            PushButton(Id("help"), "&Help"),
            PushButton(Id("ok"), "&OK"),
            PushButton(Id("cancel"), "&Cancel"),
            PushButton(Id("apply"), "&Apply")
          )
        )
      )
      UI.UserInput()
      UI.CloseDialog()

ButtonBox1Client().main()
