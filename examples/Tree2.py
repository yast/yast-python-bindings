from __future__ import unicode_literals
# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *
class Tree2Client:
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
        VBox(
          MinHeight(
            14,
            Tree(
              Id("dest_dir"),
              Opt("notify"),
              "Select destination directory:",
              [
                Item(
                  Id("root"),
                  "/",
                  True,
                  [
                    Item(
                      Id("etc"),
                      "etc",
                      [Item("opt"), Item("SuSEconfig"), Item("X11")]
                    ),
                    Item(
                      Id("usr"),
                      "usr",
                      False,
                      [
                        "bin",
                        "lib",
                        Item("share", ["man", "info", "emacs"]),
                        Item(Id("usr_local"), "local"),
                        Item("X11R6", ["bin", "lib", "share", "man", "etc"])
                      ]
                    ),
                    Item(Id("opt"), "opt", True, ["kde", "netscape", "Office51"]),
                    Item("home"),
                    "work",
                    Item(Id("other"), "<other>")
                  ]
                )
              ]
            )
          ),
          HBox(
            PushButton(Id("sel_opt"), Opt("hstretch"), "/&opt"),
            PushButton(Id("sel_usr"), Opt("hstretch"), "/&usr"),
            PushButton(Id("sel_usr_local"), Opt("hstretch"), "/usr/&local"),
            PushButton(Id("none"), Opt("hstretch"), "none")
          ),
          HBox(
            Label("Current Value:"),
            Label(Id("echo"), Opt("outputField", "hstretch"), "?????????")
          ),
          PushButton(Id("ok"), Opt("default"), "&OK")
        )
      )

      id = None
      while True:
        id = UI.UserInput()

        if id == "sel_usr":
          UI.ChangeWidget("dest_dir", "CurrentItem", Id("usr"))
        elif id == "sel_usr_local":
          UI.ChangeWidget("dest_dir", "CurrentItem", Id("usr_local"))
        elif id == "sel_opt":
          UI.ChangeWidget("dest_dir", "CurrentItem", Id("opt"))
        elif id == "none":
          UI.ChangeWidget("dest_dir", "CurrentItem", None)

        UI.ChangeWidget("echo", "Value", "")
        current_dir = UI.QueryWidget("dest_dir", "CurrentItem")

        if current_dir != None:
          UI.ChangeWidget("echo", "Value", ycpbuiltins.sformat("%1", current_dir))

        ycpbuiltins.y2milestone("Items:\n%1", UI.QueryWidget("dest_dir", "Items"))
        ycpbuiltins.y2milestone(
          "OpenItems: %1",
          UI.QueryWidget("dest_dir", "OpenItems")
        )
        ycpbuiltins.y2milestone(
          "Current Branch: %1",
          UI.QueryWidget("dest_dir", "CurrentBranch")
        )
        if id == "ok":
          break


      # Close the dialog.
      # Remember to read values from the dialog's widgets BEFORE closing it!
      UI.CloseDialog()


Tree2Client().main()

