# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class ReplacePoint1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          ReplacePoint(Id("rp"), Label("This is a label")),
          PushButton(Id("change"), "Change")
        )
      )
      UI.UserInput()
      UI.ReplaceWidget(Id("rp"), PushButton("This is a PushButton"))
      UI.UserInput()
      UI.ReplaceWidget(Id("rp"), CheckBox("This is a CheckBox"))
      UI.UserInput()
      UI.ReplaceWidget(
        Id("rp"),
        HBox(PushButton("Button1"), PushButton("Button2"))
      )
      UI.UserInput()
      UI.CloseDialog()


ReplacePoint1Client().main()

