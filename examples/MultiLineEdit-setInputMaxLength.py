# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class MultiLineEditSetInputMaxLengthClient:
    def main(self):

      UI.OpenDialog(
        VBox(
          MultiLineEdit(Id("input"), "Multi Line Edit", "pizza\npasta\npronta"),
          IntField(Id("field"), "Limit characters to...", -1, 100, -1),
          PushButton(Id("butt"), "limit input"),
          PushButton(Id("exitButton"), "Exit")
        )
      )

      ret = None

      ret = UI.UserInput()

      while ret != "exitButton":
        chars = UI.QueryWidget(Id("field"), "Value")
        UI.ChangeWidget("input", "InputMaxLength", chars)
        ret = UI.UserInput()

      UI.CloseDialog()


MultiLineEditSetInputMaxLengthClient().main()

