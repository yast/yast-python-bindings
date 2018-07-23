from __future__ import unicode_literals
# encoding: utf-8

# Minimalistic example for tab widget
from yast import import_module
import_module('UI')
from yast import *
class DumbTab3Client:
    def main(self):
      if not UI.HasSpecialWidget("DumbTab"):
        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the DumbTab widget!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      UI.OpenDialog(
        VBox(
          DumbTab(
            Id("tab"),
            [
		Item(Id("pg1"),"Page 1"),
		Item(Id("pg2"),"Page 2"),
		Item(Id("pg3"),"Page 3")
	    ],
            RichText(Id("contents"), "Contents")
          ),
          Left(
            HBox(
              PushButton(Id("page1"), "Page &1"),
              PushButton(Id("page2"), "Page &2"),
              PushButton(Id("page3"), "Page &3")
            )
          ),
          Right(PushButton(Id("close"), "&Close"))
        )
      )

      UI.DumpWidgetTree

      UI.ChangeWidget("tab", "CurrentItem", Id("pg3"))

      input = None
      while True:
        input = UI.UserInput()

        if input:
          UI.ChangeWidget("contents", "Value", input)

        if input == "page1":
          UI.ChangeWidget("tab", "CurrentItem", Id("pg1"))
        elif input == "page2":
          UI.ChangeWidget("tab", "CurrentItem", Id("pg2"))
        elif input == "page3":
          UI.ChangeWidget("tab", "CurrentItem", Id("pg3"))

        ycpbuiltins.y2milestone(
          "Current tab: %1",
          UI.QueryWidget("tab", "CurrentItem")
        )
        if input == "close":
            break


      UI.CloseDialog()


DumbTab3Client().main()

