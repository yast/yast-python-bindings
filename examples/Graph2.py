# encoding: utf-8

# Graph2.ycp
from yast import *
class Graph2Client:
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
          HBox(
            PushButton(Id("load1"), Opt("default"), "Load 1"),
            PushButton(Id("load2"), Opt("default"), "Load 2"),
            PushButton(Id("load3"), Opt("default"), "Load 3"),
            PushButton(Id("close"), Opt("default"), "&Close")
          )
        )
      )

      while True:
        widget =UI.UserInput()

        if widget == "load1":
            UI.ChangeWidget(Id("graph"), "Filename", "graph1.gv")
        elif widget == "load2":
            UI.ChangeWidget(Id("graph"), "Filename", "graph2.gv")
        elif widget == "load3":
            UI.ChangeWidget(Id("graph"), "Filename", "graph3.gv")
        elif widget == "close" or widget == "cancel":
            break

      UI.CloseDialog()


Graph2Client().main()

