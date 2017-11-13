# encoding: utf-8

from yast import *

class CheckBox2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label("Select your extras"),
          Left(CheckBox(Id("cheese"), "Extra Cheese")),
          Left(CheckBox(Id("pepr"), "Pepperoni", True)),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      cheese = bool(UI.QueryWidget("cheese", "Value"))
      pepr = bool(UI.QueryWidget("pepr", "Value"))
      UI.CloseDialog()

      UI.OpenDialog(
        VBox(
          Left(Label("Extra Cheese: " + yesno(cheese))),
          Left(Label("Pepperoni: " + yesno(pepr))),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


def yesno(b):
  if b:
    return "yes"
  else:
    return "no"

CheckBox2Client().main()
