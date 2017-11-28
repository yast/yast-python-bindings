# encoding: utf-8

# ProgressBar example
from yast import import_module
import_module('UI')
from yast import *
class ProgressBar2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("Adjust the volume"),
          ProgressBar(Id("vol"), "Volume", 100, 50),
          HBox(
            PushButton(Id("down"), "<<"),
            PushButton(Id("up"), ">>"),
            HStretch(),
            HSpacing(3),
            PushButton(Id("cancel"), "&Close")
          )
        )
      )

      while True:
        button = UI.UserInput()

        if button == "cancel":
          break
        elif button == "down" or button == "up":
          volume = UI.QueryWidget(Id("vol"), "Value")

          if button == "down":
            volume = volume - 5
          if button == "up":
            volume = volume + 5

          ycpbuiltins.y2milestone("Volume: %1", volume)
          UI.ChangeWidget(Id("vol"), "Value", volume)

      UI.CloseDialog()


ProgressBar2Client().main()

