# encoding: utf-8

from yast import *

# Example for CheckBoxFrame with inverted check box:
# The frame content becomes active if the check box is off
class CheckBoxFrame2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MarginBox(
            1,
            0.5,
            CheckBoxFrame(
              Opt("invertAutoEnable"),
              "&Automatic",
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

CheckBoxFrame2Client().main()
