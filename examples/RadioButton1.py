from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class RadioButton1Client:
    def main(self):
      UI.OpenDialog(
        RadioButtonGroup(
          Id("rb"),
          VBox(
            Label("How do you want to crash?"),
            Left(RadioButton(Id(0), "No&w")),
            Left(RadioButton(Id(1), "&Every now and then")),
            Left(RadioButton(Id(2), "Every &five minutes", True)),
            Left(RadioButton(Id(3), Opt("boldFont"), "Ne&ver", True)),
            HBox(PushButton(Id("next"), "&Next"), PushButton("&OK"))
          )
        )
      )

      while True:
        ret = UI.UserInput()
        if ret == "next":
          current = UI.QueryWidget(Id("rb"), "CurrentButton")
          current = ((current + 1) % 4)
          UI.ChangeWidget(Id("rb"), "CurrentButton", current)
        else:
          break

      UI.CloseDialog()


RadioButton1Client().main()

