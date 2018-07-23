from __future__ import unicode_literals
# encoding: utf-8

# PushButton with icons (relative path)
from yast import import_module
import_module('UI')
from yast import *
class IconButton1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          Heading("YaST2 Mini Control Center"),
          IconButton(Id("keyboard "), "yast-keyboard.png", "Keyboard"),
          IconButton(Id("mouse"), "yast-mouse.png", "Mouse"),
          IconButton(Id("timezone"), "yast-timezone.png", "Time zone"),
          IconButton(Id("lan"), "yast-lan.png", "Network"),
          IconButton(Id("sw_single"), "yast-software.png", "Software")
        )
      )

      ret = None
      while True:
        ret = UI.UserInput()

        if ret != "cancel":
          UI.OpenDialog(
            Label("Running " + ret + "...")
          )
          ycpbuiltins.sleep(4000)
          UI.CloseDialog()
        if ret == "cancel":
          break

      UI.CloseDialog()


IconButton1Client().main()

