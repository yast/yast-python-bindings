# encoding: utf-8

from yast import *
class Enabling1Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          PushButton(Id("test"), Opt("hstretch", "disabled"), "Disabled"),
          PushButton(Id("change"), Opt("hstretch"), "&Change")
        )
      )

      enabled = False

      while (UI.UserInput() != "cancel"):
        enabled = not enabled
        UI.ChangeWidget(Id("test"), "Enabled", enabled)

        if enabled:
          UI.ChangeWidget(Id("test"), "Label", "Enabled")
        else:
          UI.ChangeWidget(Id("test"), "Label", "Disabled")
      UI.CloseDialog()


Enabling1Client().main()

