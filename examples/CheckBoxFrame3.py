from __future__ import unicode_literals
# encoding: utf-8
import ycpbuiltins
from yast import import_module
import_module('UI')
from yast import *

# Example for CheckBoxFrame without auto enable:
# The application has to handle the check box
class CheckBoxFrame3Client:
    def main(self):
      UI.OpenDialog(
        VBox(
          MarginBox(
            1,
            0.5,
            CheckBoxFrame(
              Id("use_suse_server"),
              Opt("noAutoEnable", "notify"),
              "&SuSE Server",
              False,
              VBox(
                HBox(
                  InputField(Id("server"), "&Server"),
                  ComboBox(Id("mode"), "&Mode", ["Automatic", "Manual", "Debug"])
                ),
                Left(Id("logging"), CheckBox("&Logging")),
                InputField(Id("connections"), "&Connections")
              )
            )
          ),
          PushButton(Id("ok"), "&OK")
        )
      )

      widget = None
      old_server = ""
      UI.FakeUserInput("use_suse_server")
      while True:
        widget = UI.UserInput()

        if widget == "use_suse_server":
          ycpbuiltins.y2debug("Changing enabled states")
          use_suse_server = UI.QueryWidget("use_suse_server", "Value")
          UI.ChangeWidget("server", "Enabled", not use_suse_server)
          UI.ChangeWidget("mode", "Enabled", not use_suse_server)

          if use_suse_server:
            old_server = UI.QueryWidget("server", "Value")
            UI.ChangeWidget("server", "Value", "ftp://ftp.opensuse.org")
          else:
            UI.ChangeWidget("server", "Value", old_server)
        if widget == "ok" or widget == "cancel":
            break

      UI.CloseDialog()

CheckBoxFrame3Client().main()
