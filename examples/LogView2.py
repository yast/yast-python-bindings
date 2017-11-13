# encoding: utf-8

from yast import *
class LogView2Client:
    def main(self):

      button = None


      UI.OpenDialog(
        VBox(
          LogView(
            Id("log"),
            "Log View ",
            15, # visible lines
            0
          ), # lines to store
          PushButton(Id("ok"), "&OK")
        )
      )
      while True:
        line = ycpbuiltins.tostring(ycpbuiltins.random(100))
        line = line + "\n"
        UI.ChangeWidget(Id("log"), "LastLine", line)
        button = UI.TimeoutUserInput(100)
        if button == "ok":
          break

      UI.CloseDialog()


LogView2Client().main()

