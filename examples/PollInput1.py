from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class PollInput1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Label(Id("lab"), "Money: 800 Euro"),
          PushButton(Id("cancel"), Opt("hstretch"), "Cancel"),
          PushButton(Id("add"), Opt("hstretch"), "Add 50")
        )
      )
      num = 800
      UI.NormalCursor()

      while num > 0:
        ret = UI.PollInput()
        ycpbuiltins.y2milestone("%1", ret)
        if ret == "cancel":
          break
        elif ret == "add":
          num = num + 50
        UI.ChangeWidget(
          Id("lab"),
          "Value",
          "Money: " + str(num) + " Euro"
        )
        ycpbuiltins.sleep(500)
        num = num - 1
      UI.CloseDialog()


PollInput1Client().main()

