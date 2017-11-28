# encoding: utf-8
from yast import import_module
import_module('UI')
from yast import *

class CheckBox4Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label("Select your extras"),
          Left(CheckBox(Id("cheese"), "Extra Cheese")),
          Left(CheckBox(Id("pepr"), "Pepperoni", True)),
          Left(CheckBox(Id("salami"), Opt("boldFont"), "Extra Salami")),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      cheese = UI.QueryWidget("cheese", "Value")
      pepr = UI.QueryWidget("pepr", "Value")
      salami = UI.QueryWidget("salami", "Value")
      UI.CloseDialog()

      UI.OpenDialog(
        VBox(
          Left(Label("Extra Cheese: " + yesno(cheese))),
          Left(Label("Pepperoni: " + yesno(pepr))),
          Left(Label("Extra Salami: " + yesno(salami))),
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

CheckBox4Client().main()
