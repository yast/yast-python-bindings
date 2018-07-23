#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
from yast import import_module
import_module('UI')
from yast import *

# Simple example how to use background pixmaps in alignments
class BackgroundPixmapClient:
    def main(self):
      l = List()
      UI.OpenDialog(
        Opt("defaultsize"),
        VBox(
          HVCenter(
            #term("BackgroundPixmap", "wallpapers/welcome.jpg"),
            Term("BackgroundPixmap", "/usr/share/wallpapers/Mountains.jpg"),
            MinSize(20, 7, SelectionBox("", ["English", "Italiano", "Klingon"]))
          ),
          Right(PushButton(Opt("default"), "&Close"))
        )
      )
      UI.UserInput()
      UI.CloseDialog()

BackgroundPixmapClient().main()
