# encoding: utf-8

from yast import *
class Enabling2Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          InputField(Id("test"), Opt("disabled"), "TestEntry", "Disabled"),
          PushButton(Id("change"), Opt("hstretch"), "&Change")
        )
      )

      enabled = False

      while (UI.UserInput() != "cancel"):
        enabled = not enabled
        UI.ChangeWidget(Id("test"), "Enabled", enabled)

        if enabled:
          UI.ChangeWidget(Id("test"), "Value", "Enabled")
        else:
          UI.ChangeWidget(Id("test"), "Value", "Disabled")
      UI.CloseDialog()

Enabling2Client().main()

