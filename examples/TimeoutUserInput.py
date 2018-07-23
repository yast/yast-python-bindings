from __future__ import unicode_literals
# encoding: utf-8

# TimeoutUserInput.ycp
#
# Example for common usage of UI::TimeoutUserInput()
from yast import import_module
import_module('UI')
from yast import *
class TimeoutUserInputClient:
    def main(self):
      # Build dialog with two labels and an "OK" button.

      countdown_sec = 30
      interval_millisec = 200
      countdown = (countdown_sec * 1000) / interval_millisec


      UI.OpenDialog(
        VBox(
          Label("Rebooting Planet Earth..."),
          Label(Id("seconds"), ycpbuiltins.sformat("%1", countdown_sec)),
          PushButton(Id("ok"), Opt("default"), "&OK")
        )
      )

      id = None
      while True:
        id = UI.TimeoutUserInput(interval_millisec)

        if id == "timeout":
          # Periodic screen update

          countdown = countdown - 1
          seconds_left = (countdown * interval_millisec) / 1000

          UI.ChangeWidget(
            Id("seconds"),
            "Value",
            ycpbuiltins.sformat("%1", seconds_left)
          )
        if id == "ok" or countdown < 0:
          break

      UI.CloseDialog()


TimeoutUserInputClient().main()

