# encoding: utf-8

from yast import *
class InputFieldSetInputMaxLengthClient:
    def main(self):

      UI.OpenDialog(
        VBox(
          InputField(Id("input"), "Input Field", "pizza, pasta, pronta"),
          IntField(Id("field"), "Limit characters to...", -1, 100, -1),
          PushButton(Id("butt"), "limit input"),
          PushButton(Id("exitButton"), "Exit")
        )
      )

      ret = None

      ret = UI.UserInput()

      while (ret != "exitButton"):
        chars = UI.QueryWidget(Id("field"), "Value")
        UI.ChangeWidget("input", "InputMaxLength", chars)
        ret = UI.UserInput()

      UI.CloseDialog()


InputFieldSetInputMaxLengthClient().main()

