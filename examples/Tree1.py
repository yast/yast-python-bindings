from __future__ import unicode_literals
# encoding: utf-8

# Simple tree example
from yast import import_module
import_module('UI')
from yast import *
class Tree1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MinSize(
            30,
            10,
            Tree(
              Id("dest_dir"),
              "Select destination directory:",
              [
                Item(
                  Id("root"),
                  "/",
                  False,
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
                    Item(
                      Id("opt"),
                      "opt",
                      False,
                      ["kde", "netscape", "Office51"]
                    ),
                    Item("home", False),
                    Item(Id("other"), "<other>")
                  ]
                )
              ]
            )
          ),
          HBox(
            PushButton(Id("sel_opt"), Opt("hstretch"), "/&opt"),
            PushButton(Id("sel_usr"), Opt("hstretch"), "/&usr"),
            PushButton(Id("sel_usr_local"), Opt("hstretch"), "/usr/&local")
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
        if id == "ok":
          break

      # Get the input from the tree.
      #
      # Notice: The return value of UI::UserInput() does NOT return this value!
      # Rather, it returns the ID of the widget (normally the PushButton)
      # that caused UI::UserInput() to return.
      dest_dir = UI.QueryWidget("dest_dir", "CurrentItem")
      ycpbuiltins.y2debug("Selected: %1", dest_dir)


      if dest_dir == None:
        dest_dir = ""

      # Close the dialog.
      # Remember to read values from the dialog's widgets BEFORE closing it!
      UI.CloseDialog()


      # Pop up a new dialog to echo the selection.
      UI.OpenDialog(
        VBox(
          Label(
            ycpbuiltins.sformat("Selected destination directory: %1", dest_dir)
          ),
          PushButton(Opt("default"), "&OK")
        )
      )
      UI.UserInput()

      UI.CloseDialog()


Tree1Client().main()

