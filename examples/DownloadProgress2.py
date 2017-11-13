# encoding: utf-8

from yast import *
class DownloadProgress2Client:
    def main(self):
      # Check for availability of special widgets required for this example

      if not UI.HasSpecialWidget("DownloadProgress"):
        UI.OpenDialog(
          VBox(
            Label("Error: This UI doesn't support the DownloadProgress widget!"),
            PushButton(Opt("default"), "&OK")
          )
        )
        UI.UserInput()
        UI.CloseDialog()

        return


      # Initialize some (pretty random) demo values

      logfile_name = "/suse/sh/.y2log"
      # string  logfile_name = "/var/log/y2log";
      logfile_expected_size = 20 * 1024


      # Build a dialog with a download progress bar
      # and a row of some buttons below.
      #
      # The weights for will make the buttons the same size - except the last
      # one, "Close", which is deliberately set apart from the others with some
      # empty space.

      UI.OpenDialog(
        VBox(
          DownloadProgress(
            Id("progress"),
            "YaST2 log file",
            logfile_name,
            logfile_expected_size
          ),
          HBox(
            HWeight(1, PushButton(Id("y2log"), "YaST2 Log &File")),
            HWeight(1, PushButton(Id("null"), "&No File")),
            HWeight(1, PushButton(Id("blurb"), Opt("default"), "&Log Something")),
            HSpacing(Opt("hstretch"), 2),
            PushButton(Id("close"), "&Close")
          )
        )
      )

      # Input loop

      button = None
      while True:
        button = UI.UserInput()

        if button == "y2log":
          # Watch the Y2 log file

          UI.ChangeWidget(Id("progress"), "Filename", logfile_name)
          UI.ChangeWidget(Id("progress"), "ExpectedSize", logfile_expected_size)
        elif button == "null":
          # Watch no file - i.e. reset the progress bar

          UI.ChangeWidget(Id("progress"), "Filename", "")
          UI.ChangeWidget(Id("progress"), "ExpectedSize", 1024)
        elif button == "blurb":
          # log something so the log file grows

          i = 0

          while (i < 100):
            ycpbuiltins.y2milestone("Blurb - %1", i)
            i = i + 1
        if button == "close":
            break


      # Clean up

      UI.CloseDialog()


DownloadProgress2Client().main()

