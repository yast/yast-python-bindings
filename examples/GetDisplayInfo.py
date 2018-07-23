from __future__ import unicode_literals
# encoding: utf-8

# Simple demo for the UI::GetDisplayInfo() UI bultin:
#
# Open a RichText widget with all the info map's contents and format them as HTML
#
from yast import import_module
import_module('UI')
from yast import *
class GetDisplayInfoClient:
    def main(self):
      info_map = UI.GetDisplayInfo()
      info_text = "<ul>"

      for capability, value in ycpbuiltins.foreach(info_map).iteritems():
        info_text = info_text + ycpbuiltins.sformat("<li>%1: %2</li>", capability, value)

      info_text = info_text + "<ul>"

      UI.OpenDialog(
        VBox(
          HSpacing(40), # force width
          Left(Heading("Display capabilities:")),
          HBox(
            RichText(info_text), # force height
            VSpacing(15)
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()
      UI.CloseDialog()


GetDisplayInfoClient().main()

