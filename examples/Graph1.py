from __future__ import unicode_literals
# encoding: utf-8

# Graph1.ycp
from yast import import_module
import_module('UI')
from yast import *
class Graph1Client:
    def main(self):
      if not UI.HasSpecialWidget("Graph"):
        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the Graph widget!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()
        return

      UI.OpenDialog(
        VBox(
          HSpacing(60),
          Term("Graph", Id("graph"), "graph1.gv", "dot"),
          PushButton(Id("close"), Opt("default"), "&Close")
        )
      )

      while True:
        widget = UI.UserInput()

        if widget == "close" or widget == "cancel":
          break

      UI.CloseDialog()


Graph1Client().main()

