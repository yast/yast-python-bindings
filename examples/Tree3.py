from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Tree3Client:
    def main(self):
      # Build a dialog with a tree for directory selection, three
      # buttons with common values and a label that directly echoes any
      # selected directory.
      #
      # The tree in this example uses the `notify option that makes
      # UI::UserInput() return immediately as soon as the user selects a
      # tree item rather than the default behaviour which waits for the
      # user to activate a button.

      UI.OpenDialog(
        MinWidth(
          50,
          VBox(
            Tree(
              Id("dest_dir"),
              Opt("notify"),
              "Select destination directory:",
              [
                Item(
                  "/",
                  True,
                  [
                    Item("etc", [Item("opt"), Item("SuSEconfig"), Item("X11")]),
                    Item(
                      "usr",
                      False,
                      [
                        "bin",
                        "lib",
                        Item("share", ["man", "info", "emacs"]),
                        Item("local"),
                        Item("X11R6", ["bin", "lib", "share", "man", "etc"])
                      ]
                    ),
                    Item("opt", True, ["kde", "netscape", "Office51"]),
                    Item("home"),
                    "work",
                    Item("<other>")
                  ]
                )
              ]
            ),
            HBox(
              PushButton(Id("sel_opt"), Opt("hstretch"), "/&opt"),
              PushButton(Id("sel_usr"), Opt("hstretch"), "/&usr"),
              PushButton(Id("sel_usr_local"), Opt("hstretch"), "/usr/&local")
            ),
            HBox(
              HWeight(2, Label("Current Item:")),
              HWeight(5, Label(Id("echoItem"), Opt("outputField", "hstretch"), ""))
            ),
            HBox(
              HWeight(2, Label("Current Branch:")),
              HWeight(
                5,
                Label(Id("echoBranch"), Opt("outputField", "hstretch"), "")
              )
            ),
            HBox(
              HWeight(2, Label("Current Path:")),
              HWeight(5, Label(Id("echoPath"), Opt("outputField", "hstretch"), ""))
            ),
            PushButton(Id("ok"), Opt("default"), "&OK")
          )
        )
      )

      id = None
      while True:
        id = UI.UserInput()

        if id == "sel_usr":
          UI.ChangeWidget(Id("dest_dir"), "CurrentItem", "usr")
        elif id == "sel_usr_local":
          UI.ChangeWidget(Id("dest_dir"), "CurrentItem", "local")
        elif id == "sel_opt":
          UI.ChangeWidget(Id("dest_dir"), "CurrentItem", "opt")
        elif id == "dest_dir":
          current_dir = UI.QueryWidget("dest_dir", "CurrentItem")

          if current_dir != None:
            UI.ChangeWidget(
              Id("echoItem"),
              "Value",
              ycpbuiltins.sformat("%1", current_dir)
            )

          current_branch = UI.QueryWidget("dest_dir", "CurrentBranch")

          if current_branch != None:
            UI.ChangeWidget(
              "echoBranch",
              "Value",
              ycpbuiltins.sformat("%1", current_branch)
            )

            current_path = ycpbuiltins.mergestring(current_branch, "/")
            if ycpbuiltins.size(current_path) > 2:
              # Remove duplicate "/" at start
              current_path = ycpbuiltins.substring(
                current_path,
                1,
                ycpbuiltins.size(current_path) - 1)

            UI.ChangeWidget(
              "echoPath",
              "Value",
              ycpbuiltins.sformat("%1", current_path)
            )
        if id == "ok":
          break


      # Close the dialog.
      # Remember to read values from the dialog's widgets BEFORE closing it!
      UI.CloseDialog()


Tree3Client().main()

