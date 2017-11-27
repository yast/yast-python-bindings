# encoding: utf-8
from yast import *

class CheckBoxFrame1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MarginBox(
            1,
            0.5,
            CheckBoxFrame(
              "E&xpert Settings",
              True,
              VBox(
                HBox(
                  InputField("&Server"),
                  ComboBox("&Mode", ["Automatic", "Manual", "Debug"])
                ),
                Left(CheckBox("&Logging")),
                InputField("&Connections")
              )
            )
          ),
          PushButton("&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()

CheckBoxFrame1Client().main()
