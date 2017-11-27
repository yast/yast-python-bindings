# encoding: utf-8

from yast import import_module
import_module('UI')
from yast import *

class CheckBoxFrame4Client:
    def main(self):
      frame = VBox(
        CheckBoxFrame(
          Id("foo"),
          Opt("notify"),
          "Selection A",
          True,
          VBox(
            CheckBox("Enable Foo"),
            HBox(
              HSpacing(2),
              Left(
                CheckBoxFrame(
                  Id("bar"),
                  "Selection B",
                  False,
                  VBox(
                    CheckBox("Enable Bar"),
                    SelectionBox(Id("sel"), "Select", ["Foo", "Bar", "Baz"]),
                    CheckBoxFrame(
                      Id("c"),
                      "Selection C",
                      True,
                      CheckBox("Another")
                    )
                  )
                )
              )
            ),
            CheckBox("Disable Blubber")
          )
        ),
        PushButton(Id("ok"), "OK")
      )

      UI.OpenDialog(frame)

      id = None
      while True:
        id = UI.UserInput()
        if id == "ok":
          break

      UI.CloseDialog()

CheckBoxFrame4Client().main()
